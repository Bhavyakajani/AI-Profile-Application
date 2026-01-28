// profile_test.js
import http from 'k6/http';
import { sleep } from 'k6';


export let options = {
  vus: 200,
  duration: '30s',
};

export default function () {
  http.get('http://localhost:8000/profile/');
  sleep(1);
}

export { handleSummary } from './summary.js';
