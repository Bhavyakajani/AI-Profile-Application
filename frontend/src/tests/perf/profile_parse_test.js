import http from 'k6/http';
import { sleep } from 'k6';

/**
 * LLM-safe load configuration
 * Gradual ramp-up, low concurrency
 */
export let options = {
  stages: [
    { duration: '15s', target: 3 },
    { duration: '30s', target: 6 },
    { duration: '30s', target: 9 },
    { duration: '15s', target: 0 },
  ],
  thresholds: {
    http_req_failed: ['rate<0.05'],      // <5% failures
    http_req_duration: ['p(95)<60000'],  // 95% < 10s (LLM realistic)
  },
};

// Preload files ONCE (important for performance)
const resumes = [
  open('./data/resume_1.pdf', 'b'),
  open('./data/resume_2.pdf', 'b'),
  open('./data/resume_3.pdf', 'b'),
  open('./data/resume_4.pdf', 'b'),
  open('./data/resume_5.pdf', 'b'),
  open('./data/resume_6.pdf', 'b'),
  open('./data/resume_7.pdf', 'b'),
  open('./data/resume_8.pdf', 'b'),
  open('./data/resume_9.pdf', 'b'),
];

export default function () {
  // 🔁 Rotate files deterministically
  const fileIndex = (__VU + __ITER) % resumes.length;

  const payload = {
    file: http.file(
      resumes[fileIndex],
      `resume_${fileIndex + 1}.pdf`,
      'application/pdf'
    ),
  };

  const params = {
    headers: {
      Authorization: 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJrYWphbmliaGF2eWFAZ21haWwuY29tIiwiZXhwIjoxNzY5NTcyNjE3fQ.BMuFKDM4DppgB2WsDyvgsuRygN9YeqWPiqgWiwZsYrU',
    },
    timeout: '60s', // LLM safety
  };

  const res = http.post(
    'http://localhost:8000/profile/parse',
    payload,
    params
  );

  // Think time — DO NOT remove for LLM endpoints
  sleep(3);
}

export { handleSummary } from './summary.js';
