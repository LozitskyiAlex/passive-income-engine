export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/sitemap.xml") {
      const sitemapUrl = new URL("/sitemap.xml", url.origin);
      const response = await env.ASSETS.fetch(
        new Request(sitemapUrl.toString(), {
          method: "GET",
          headers: {
            "Accept": "application/xml,text/xml;q=0.9,*/*;q=0.8",
            "Cache-Control": "no-cache",
          },
        }),
      );

      const body = await response.text();

      return new Response(body, {
        status: 200,
        headers: {
          "Content-Type": "application/xml; charset=UTF-8",
          "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
          "Pragma": "no-cache",
          "X-Robots-Tag": "noindex",
        },
      });
    }

    return env.ASSETS.fetch(request);
  },
};
