# Google AdSense activation checklist

The site build now adds the AdSense publisher verification script to every generated content page across all fifteen locales and creates the root `/ads.txt` file.

Publisher ID: `pub-7560850346426622`

## Complete setup in AdSense

1. Open the AdSense account and add `https://free-construction-calculators.pages.dev` under **Sites**.
2. Select the AdSense code verification method if requested. The publisher script is already included in the generated page HTML.
3. Confirm that `https://free-construction-calculators.pages.dev/ads.txt` returns:
   
   `google.com, pub-7560850346426622, DIRECT, f08c47fec0942fa0`

4. In **Privacy & messaging**, configure the European regulations message. For personalized ads in the EEA, UK and Switzerland, Google requires a Google-certified CMP integrated with the IAB Transparency and Consent Framework.
5. Publish a privacy policy that accurately describes Google's advertising cookies, data processing and third-party ad technology providers.
6. In AdSense, request the site review and wait until the site status is **Ready**.
7. If using Auto ads, enable and configure them in AdSense after approval. Loading the publisher script alone does not create ad placements or guarantee that ads will appear.

## Important

The code integration does not mean Google has approved the site or enabled ad serving. Ad serving is subject to Google's review, account status, site policies and consent configuration.

The current site uses a Cloudflare Pages subdomain. If AdSense does not accept it during site registration or ownership verification, connect a custom domain that you control to the Cloudflare Pages project and add that domain to AdSense.
