const Config = require("./secret.hidden.json");
const SnowTransfer = new (require("snowtransfer"))(Config.token, {});

(async () => {
    console.log(await SnowTransfer.channel.getChannelMessages("530101234590547968", {"limit": 100}));
})().catch(console.error);