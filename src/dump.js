const Config = require("../secret.hidden.json");
const SnowTransfer = new (require("snowtransfer"))(Config.token, {});
const limit = 100;
const {promises: fs} = require("fs");

/** @param {Array.<import("@amanda/discordtypings").MessageData>} Data */
const ShaveData = async (Data) => {
    const Cache = [];
    for (const Message of Data) {
        Cache.push({"id": Message.id, "embeds": Message.embeds, "timestamp": Message.timestamp});
    }
    return Cache;
};

(async () => {
    let Count = 1;
    let Cache = null;
    let BeforeOffset;
    const File = await fs.open(`${(new Date).toISOString()}.txt`, "ax");
    await File.appendFile("Start of messages dump\n");
    Cache = await SnowTransfer.channel.getChannelMessages("530101234590547968", {"limit": limit});
    BeforeOffset = Cache[limit - 1].id;
    await File.appendFile(`${JSON.stringify(await ShaveData(Cache))}\n`);
    console.log(`Next snowflake: ${BeforeOffset}\nCount: ${Count}\n`);
    // eslint-disable-next-line no-constant-condition
    while (true) {
        Count += 1;
        Cache = await SnowTransfer.channel.getChannelMessages("530101234590547968", {"limit": limit, "before": BeforeOffset});
        BeforeOffset = Cache[limit - 1].id;
        await File.appendFile(`${JSON.stringify(await ShaveData(Cache))}\n`);
        console.log(`Next snowflake: ${BeforeOffset}\nCount: ${Count}\n`);
    }
})().catch(console.error);