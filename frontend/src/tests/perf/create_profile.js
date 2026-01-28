import http from 'k6/http';
import { sleep } from 'k6';

export let options = {
  vus: 200,
  duration: '20s',
};

export default function () {
  // 🔑 UNIQUE identifiers per request
  const uniqueId = `${__VU}-${__ITER}-${Date.now()}`;

  const payload = JSON.stringify({
    name: `Test Profile ${uniqueId}`,
    email: `test_${uniqueId}@example.com`,
    contact_number: `12345${__VU}${__ITER}`,
    skills: ["Python", "FastAPI"],
    education: [
      {
        degree: 'BSc Computer Science',
        institution: 'Warsaw University of Technology',
        start_date: '2021-09-01',
        end_date: '2025-06-30',
        location: 'Warsaw, Poland',
        cgpa: '4.5',
      }
    ],
    YoE: "3"
  });

  const params = {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJrYWphbmliaGF2eWFAZ21haWwuY29tIiwiZXhwIjoxNzY5NTcwNjk0fQ.dofiyAZHIIr_GxYgGov2IBJAewkOXFwgHtHkfushDk0'
    }
  };

  http.post('http://localhost:8000/profile/', payload, params);
  sleep(1);
}

export { handleSummary } from './summary.js';