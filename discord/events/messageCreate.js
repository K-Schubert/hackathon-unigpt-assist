const {Events} = require("discord.js");
// use : npm install node-fetch@2
const fetch = require('node-fetch');
// otherwise ...
// import fetch from 'node-fetch';
// ES Modules (ESM) etc...

let url_api = 'http://unigpt-assist.westeurope.azurecontainer.io/rag/'

const regexPrefix = new RegExp('unigpt*');

module.exports = {
    name: Events.MessageCreate,
    async execute(msg) {
        if (regexPrefix.test(msg.content)) {
            console.log('unigpt event');
            // change the arg to correspond to the regexPrefix length
            const message = msg.content.substring(6);
            console.log(message);
            // https://www.npmjs.com/package/node-fetch
            /*
            const callResult = await fetch(url_api, {
                method : 'post',
                body : JSON.stringify(message),
                headers: {'Content-Type': 'application/json}'},
            });*/
            //
            // const callResult = await fetch(url_api, {
            //     method : 'POST',
            //     body : `message=${message}`
            // });
            // with form params
            const params = new URLSearchParams();
            params.append('message', message);
            const callResult = await fetch(url_api,
                {
                    method: 'POST',
                    body: params
                });
            // console.log(callResult);

            const data = await callResult.json();
            // const body = await callResult.text();

            // console.log(data);

            const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
            await delay(1000);

            // await msg.reply(watsonResponse)
            await msg.reply(data.answer)
                .then(() => console.log(`Replied to message "${msg.content}"`))
                .catch(console.error);
        }
    }
};
