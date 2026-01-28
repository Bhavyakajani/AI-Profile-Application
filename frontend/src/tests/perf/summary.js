import { htmlReport } from "https://raw.githubusercontent.com/benc-uk/k6-reporter/main/dist/bundle.js";
import { textSummary } from "https://jslib.k6.io/k6-summary/0.0.4/index.js";

export function handleSummary(data) {
  return {
    "C:/Users/tonyj/OneDrive/Desktop/Sem8/Thesis/Performance testing results/k6/profile_parse_summary.html":
      htmlReport(data),
    stdout: textSummary(data, { indent: " ", enableColors: true }),
  };
}
