// ============================================================
// Hiring Marketplace Analytics — Google Apps Script
// ============================================================
// How to use:
//   1. In your Google Sheet go to Extensions > Apps Script
//   2. Delete the default function and paste this entire file
//   3. Run addSimulatedJourneys once to test (approve permissions)
//   4. Run createTrigger once to start the 15-min schedule
//   5. Run deleteTriggers when you're done to stop the schedule
//   6. Deploy > New deployment > Web app to get the JSON endpoint
// ============================================================

const SHEET_NAME = 'funnel';

// Reads the header row and returns a map of column name -> index
function headerIndex_(sh) {
  const header = sh.getRange(1, 1, 1, sh.getLastColumn()).getValues()[0];
  const idx = {};
  header.forEach((h, i) => { idx[h] = i; });
  return { header: header, idx: idx };
}

// Monday of the week for a date, as yyyy-MM-dd
function weekStart_(d, tz) {
  const dayNum = Number(Utilities.formatDate(d, tz, 'u')); // 1 = Monday
  const monday = new Date(d.getTime() - (dayNum - 1) * 86400000);
  return Utilities.formatDate(monday, tz, 'yyyy-MM-dd');
}

// Appends N simulated journeys by cloning recent rows and shifting timestamps to "now"
function addSimulatedJourneys() {
  const N = 25;
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sh = ss.getSheetByName(SHEET_NAME);
  const tz = ss.getSpreadsheetTimeZone();
  const info = headerIndex_(sh);
  const header = info.header, idx = info.idx;

  const lastRow = sh.getLastRow();
  const sampleStart = Math.max(2, lastRow - 2999);
  const sample = sh.getRange(sampleStart, 1, lastRow - sampleStart + 1, header.length).getValues();

  const now = new Date();
  const tsCols = ['viewed_at', 'applied_at', 'recruiter_viewed_at',
                  'recruiter_responded_at', 'interviewed_at', 'hired_at'];
  const out = [];
  for (let i = 0; i < N; i++) {
    const row = sample[Math.floor(Math.random() * sample.length)].slice();
    const oldView = row[idx['viewed_at']];
    if (!(oldView instanceof Date)) continue;   // skip rows whose timestamp was not parsed
    const delta = now.getTime() - oldView.getTime();
    tsCols.forEach(function (c) {
      if (row[idx[c]] instanceof Date) row[idx[c]] = new Date(row[idx[c]].getTime() + delta);
    });
    row[idx['journey_id']] = 'JR' + now.getTime() + '_' + i;
    row[idx['view_date']] = Utilities.formatDate(now, tz, 'yyyy-MM-dd');
    row[idx['view_week']] = weekStart_(now, tz);
    out.push(row);
  }
  if (out.length) {
    sh.getRange(sh.getLastRow() + 1, 1, out.length, header.length).setValues(out);
  }
  Logger.log('Added ' + out.length + ' simulated journeys.');
}

// Run once to start the schedule (adds records every 15 minutes)
function createTrigger() {
  ScriptApp.newTrigger('addSimulatedJourneys').timeBased().everyMinutes(15).create();
  Logger.log('Trigger created. addSimulatedJourneys will run every 15 minutes.');
}

// Run once to stop all triggers (do this after your demo recording)
function deleteTriggers() {
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(function (t) { ScriptApp.deleteTrigger(t); });
  Logger.log('Deleted ' + triggers.length + ' trigger(s).');
}

// Web app endpoint: returns headline KPIs as JSON
// Deploy > New deployment > Web app, Execute as: Me, Who has access: Anyone
function doGet() {
  const sh = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME);
  const idx = headerIndex_(sh).idx;
  const n = sh.getLastRow() - 1;   // total rows excluding header = total views
  const sum = function (name) {
    return sh.getRange(2, idx[name] + 1, n, 1).getValues()
             .reduce(function (a, r) { return a + (Number(r[0]) || 0); }, 0);
  };
  const applies = sum('applied'), responded = sum('responded'), hired = sum('hired');
  const result = {
    generated_at: new Date().toISOString(),
    views: n,
    applies: applies,
    responded: responded,
    hired: hired,
    view_to_apply_pct: Number((100 * applies / n).toFixed(1)),
    response_pct: Number((100 * responded / applies).toFixed(1)),
    hire_pct: Number((100 * hired / applies).toFixed(1))
  };
  return ContentService.createTextOutput(JSON.stringify(result, null, 2))
                       .setMimeType(ContentService.MimeType.JSON);
}
