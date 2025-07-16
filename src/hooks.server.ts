import { sequence } from '@sveltejs/kit/hooks';

export const handle = async ({ event, resolve }: { event: any, resolve: any }) => {
  // bypass body parsing for specific routes
  if (event.url.pathname.startsWith('/api/video/stream')) {
    event.request = event.request; // force passthrough
    return resolve(event, { maxBodySize: Infinity }); // <= important
  }

  return resolve(event);
};