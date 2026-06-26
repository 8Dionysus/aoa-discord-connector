# Discord Source Policy

This connector is a permissioned Discord conversation connector.

## Official Surfaces Checked

- Discord Gateway and Gateway intents:
  `https://discord.com/developers/docs/events/gateway`
- Discord Message resource and channel history:
  `https://discord.com/developers/docs/resources/message`
- Discord permissions:
  `https://discord.com/developers/docs/topics/permissions`
- Message Content privileged intent:
  `https://support-dev.discord.com/hc/en-us/articles/6207308062871-What-are-Privileged-Intents`
- Automated user accounts/selfbots:
  `https://support.discord.com/hc/en-us/articles/115002192352-Automated-User-Accounts-Self-Bots`
- Account-owned Data Package:
  `https://support.discord.com/hc/en-us/articles/360004957991-Your-Discord-Data-Package`

## Allowed Modes

- `bot_gateway`: bot installed in a guild with explicit channel/thread
  allowlist. Message text may be unavailable without Message Content.
- `bot_gateway_message_content`: same as above, with privileged Message Content
  intent approved/configured.
- `rest_history`: REST history / channel history backfill where bot
  permissions allow it.
- `data_package`: offline import of the connected user's own Discord Data
  Package.

## Forbidden Routes

- User-token scraping, automated user accounts, or selfbot collection.
- Live collection of arbitrary user DMs. Bot DMs and account-owned Data Package
  import are the acceptable routes.
- Write routes: send, edit, delete, react, join, invite, moderate, or reply.
- Attachments download/media download by default. Attachment metadata may be
  indexed.
- Broad unbounded guild crawling.
- Discord internal search as a crawler source.

Return `insufficient_permission` when guild/channel/message-content permissions
do not allow the requested evidence.
