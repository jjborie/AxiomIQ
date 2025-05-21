import { test } from 'node:test';
import assert from 'node:assert/strict';
import { getKus } from '../src/api.js';

test('getKus fetches /api/kus', async () => {
  let called = false;
  const fakeFetch = async (url) => {
    called = true;
    assert.equal(url, '/api/kus');
    return { ok: true, json: async () => ['a', 'b'] };
  };
  const result = await getKus(fakeFetch);
  assert.ok(called);
  assert.deepEqual(result, ['a', 'b']);
});

test('getKus throws on error response', async () => {
  const fakeFetch = async () => ({ ok: false, status: 500 });
  await assert.rejects(getKus(fakeFetch), /500/);
});
