const SITEMAP = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://passive-income-engine.oleksoleks07.workers.dev/</loc></url>
  <url><loc>https://passive-income-engine.oleksoleks07.workers.dev/construction/</loc></url>
  <url><loc>https://passive-income-engine.oleksoleks07.workers.dev/construction/concrete-volume/</loc></url>
  <url><loc>https://passive-income-engine.oleksoleks07.workers.dev/construction/concrete-bags/</loc></url>
  <url><loc>https://passive-income-engine.oleksoleks07.workers.dev/construction/gravel-volume/</loc></url>
  <url><loc>https://passive-income-engine.oleksoleks07.workers.dev/construction/mulch-volume/</loc></url>
  <url><loc>https://passive-income-engine.oleksoleks07.workers.dev/construction/paint-quantity/</loc></url>
  <url><loc>https://passive-income-engine.oleksoleks07.workers.dev/construction/flooring-quantity/</loc></url>
  <url><loc>https://passive-income-engine.oleksoleks07.workers.dev/construction/tile-quantity/</loc></url>
  <url><loc>https://passive-income-engine.oleksoleks07.workers.dev/construction/drywall-sheets/</loc></url>
  <url><loc>https://passive-income-engine.oleksoleks07.workers.dev/construction/board-feet/</loc></url>
  <url><loc>https://passive-income-engine.oleksoleks07.workers.dev/construction/material-cost/</loc></url>
  <url><loc>https://passive-income-engine.oleksoleks07.workers.dev/construction/paver-quantity/</loc></url>
  <url><loc>https://passive-income-engine.oleksoleks07.workers.dev/construction/sand-volume/</loc></url>
  <url><loc>https://passive-income-engine.oleksoleks07.workers.dev/construction/soil-volume/</loc></url>
  <url><loc>https://passive-income-engine.oleksoleks07.workers.dev/construction/fence-pickets/</loc></url>
  <url><loc>https://passive-income-engine.oleksoleks07.workers.dev/construction/fence-posts/</loc></url>
  <url><loc>https://passive-income-engine.oleksoleks07.workers.dev/construction/decking-boards/</loc></url>
  <url><loc>https://passive-income-engine.oleksoleks07.workers.dev/construction/roofing-squares/</loc></url>
  <url><loc>https://passive-income-engine.oleksoleks07.workers.dev/construction/roofing-material/</loc></url>
  <url><loc>https://passive-income-engine.oleksoleks07.workers.dev/construction/gravel-weight/</loc></url>
  <url><loc>https://passive-income-engine.oleksoleks07.workers.dev/construction/concrete-weight/</loc></url>
  <url><loc>https://passive-income-engine.oleksoleks07.workers.dev/construction/concrete-footing/</loc></url>
  <url><loc>https://passive-income-engine.oleksoleks07.workers.dev/construction/rebar-length/</loc></url>
  <url><loc>https://passive-income-engine.oleksoleks07.workers.dev/construction/gravel-bags/</loc></url>
  <url><loc>https://passive-income-engine.oleksoleks07.workers.dev/construction/baseboard/</loc></url>
  <url><loc>https://passive-income-engine.oleksoleks07.workers.dev/construction/wallpaper/</loc></url>
  <url><loc>https://passive-income-engine.oleksoleks07.workers.dev/construction/stair-risers/</loc></url>
  <url><loc>https://passive-income-engine.oleksoleks07.workers.dev/construction/asphalt-volume/</loc></url>
  <url><loc>https://passive-income-engine.oleksoleks07.workers.dev/construction/cubic-yards/</loc></url>
  <url><loc>https://passive-income-engine.oleksoleks07.workers.dev/construction/area/</loc></url>
  <url><loc>https://passive-income-engine.oleksoleks07.workers.dev/construction/volume/</loc></url>
</urlset>`;

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/sitemap.xml") {
      return new Response(SITEMAP, {
        status: 200,
        headers: {
          "Content-Type": "application/xml; charset=UTF-8",
          "Cache-Control": "no-store",
        },
      });
    }

    return env.ASSETS.fetch(request);
  },
};
