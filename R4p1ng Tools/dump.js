const Config = Object.assign(require("./config.json"), require("./secret.hidden.json"));
const SnowTransfer = new (require("snowtransfer"))(Config.token, {});
/** @type {{"limit": number, "before": number}} */
const getOptions = Config.getOptions;
const { promises: fs } = require("fs");

/** @param {Array.<import("@amanda/discordtypings").MessageData>} Data */
const ShaveData = async (Data) => {
    const Cache = [];
    for (const Message of Data) {
        Cache.push({ "id": Message.id, "embeds": Message.embeds, "timestamp": Message.timestamp });
    }
    return Cache;
};

/**
 * @param {Array} Data 
 * @param {Array} Cache 
 */
const PushData = async (Data, Cache) => {
    for (const Message of await ShaveData(Data)) {
        Cache.push(Message);
    }
};

(async () => {
    let Count = 0;
    /** @type {Array.<Array.<{ "id": number, "embeds": Array, "timestamp": Date }>>} */
    let Cache = [];
    /*try { // Silently crashes, require() actually throws an error
        Cache = JSON.parse((await fs.readFile(Config.fileName, {"encoding": "utf-8"})).toString());
        Count = Cache.dump.length / 100;
        getOptions.before = Cache.beforeOffset;
        Cache = Cache.data;
    } catch (err) {
        console.log("No resumable file found, skipping resume process", err);
    }*/
    setInterval(async () => {
        const TimeStart = new Date();
        Count += 1;
        await PushData(await SnowTransfer.channel.getChannelMessages("530101234590547968", getOptions), Cache);
        getOptions.before = Cache[Cache.length - 1].id;
        await fs.writeFile(Config.fileName, JSON.stringify({"dump": Cache, "beforeOffset": getOptions.before}));
        console.log(`Count: ${Count}\nTime taken: ${(new Date()) - TimeStart}ms\n`);
    }, 2500);
})().catch(console.error);