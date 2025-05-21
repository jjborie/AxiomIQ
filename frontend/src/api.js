export async function getKus(fetcher = fetch) {
  const resp = await fetcher('/api/kus');
  if (!resp.ok) {
    throw new Error(`Failed to fetch kus: ${resp.status}`);
  }
  return resp.json();
}
