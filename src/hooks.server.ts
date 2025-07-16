import { sequence } from '@sveltejs/kit/hooks';

export const handle = sequence(async ({ event, resolve }) => {
  return await resolve(event, {
    maxRequestSize: 5_368_709_120 // 5Gb
  } as any);
});