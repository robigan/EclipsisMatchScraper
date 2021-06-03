const Config = require("./secret.hidden.json");
const SnowTransfer = new (require("snowtransfer"))(Config.token, {});

(async () => {
    await SnowTransfer.channel.getChannelMessages("530101234590547968");
})().catch(console.error);