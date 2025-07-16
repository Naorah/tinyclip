export const handle = async ({ event, resolve }: { event: any, resolve: any }) => {
  console.log(event.url.pathname);
  // bypass body parsing for specific routes
  if (event.url.pathname.startsWith('/api/video/stream')) {
    event.request = event.request; // force passthrough
    return resolve(event, { maxBodySize: 5 * 1024 * 1024 * 1024 });
  }

  return resolve(event);
};