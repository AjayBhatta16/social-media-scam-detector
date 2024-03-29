// returns a description for a given scam type
/* 
Sources:
https://www.fbi.gov/how-we-can-help-you/safety-resources/scams-and-safety/common-scams-and-crimes/romance-scams
https://www.cftc.gov/LearnAndProtect/AdvisoriesAndArticles/RecoveryFrauds.html#:~:text=Recovery%20scams%20are%20a%20form,against%20these%20follow%2Don%20schemes.
https://www.scamnet.wa.gov.au/scamnet/Scam_types-Dating__romance-Sugar_baby_scam.htm
https://securityboulevard.com/2022/07/the-top-8-social-media-scams-you-need-to-watch-out-for/
https://vpnoverview.com/privacy/social-media/instagram-scams/
https://medium.com/scam-alert/deconstructing-the-love-spell-scam-20549b236d

*/

let types = [
    {
        name: "Romance",
        description: "Romance scams are when the scammer creates a fake profile, and seeks a \"relationship\" with potential victims. This allows them to trick the victim into sending multiple sums of money over an extended period of time. They will often claim to be working in construction, on an oil rig, or in the military in order to avoid meeting in person."
    },
    {
        name: "Account Recovery",
        description: "Account recovery scams are when the scammer will target victims of other scams, in order to get their money or hacked accounts back. They will pretend to be hackers, often impersonating legitimate organizations such as law enforcement or Scammer Payback, and trick victims into sending an advance fee for a service that does not exist."
    },
    {
        name: "Sugar Baby",
        description: "In this scam, scammers will pretend to be a \"Sugar Mama\" or \"Sugar Daddy\", looking for a sugar baby to send a weekly in allowance to in exchange for online companionship. They will use this relationship as a premise to trick victims into sending them money and/or grant the scammer access to their online banking."
    },
    {
        name: "Lottery",
        description: "In this scam, the scammer will create a fake profile claiming to be a winner of the powerball jackpot or another lottery, and offer give away a sum of their money to people who follow them or message them. Then, they use this as a premise to trick victims into revealing personal information and sending money in the form of a \"confirmation fee\"."
    },
    {
        name: "Investment",
        description: "In this scam, the scammer will use a fake profile to pose as an investor, typically in crypto, and offer to help people get started with investing. Sometimes, they will post comments saying that they will give out free money to people who message them. Other times, they will use numerous fake profiles and hijacked accounts to claim that their investor persona is helping real people make money. They will typically proceed to trick those who message them into sending an advance fee to start the investment."
    },
    {
        name: "Counterfeit Goods",
        description: "These scammers will post about various goods that they are selling, sometimes impersonating reputable brands and stores, in order trick people into sending them money to buy something that they don't really have. This includes, but is not limited to: pets, alcohol, illegal drugs, superbowl tickets, clothing items, and electronics."
    },
    {
        name: "Influencer Promotion",
        description: "These scammers will prey on prospective influencers, exploiting the fact that there are many real ways that influencers can gain fake likes/followers. They often appear legitimate by offering elaborate pricing plans, and populating their profile with staged before-and-after posts. They will sometimes offer to help users get verified as well."
    },
    {
        name: "Spellcasting",
        description: "These scammers will set up fake profiles posing as spiritual doctors, offering to cast spells in exchange for a fee that covers the ingredients for the spell. They often offer a wide variety of spells, including spells that will make people fall in love, spells that cure disease, and spells that bring financial prosperity. "
    },
    {
        name: 'Fake Follower',
        description: 'This account has most likely been created for the purpose of inflating the number of likes or amount of engagement on another account. While these accounts are typically unresponsive, their impact may help scam accounts reach more victims.'
    },
    {
        name: 'Political Spammer',
        description: 'This account is most likely being used to spam political content. While the account may not be targeting people for wire fraud, they typically retweet specific canditates and activists, which could facilitate the spread of harmful misinformation.'
    },
    {
        name: 'Promotional Spammer (Apps/Services)',
        description: 'This account is most likely being used to spam promotions regarding apps and services. Many of these apps are created with the intent of committing malicious acts towards the people who download them, such as theft and unwanted device surveillance. Many of the services being promoted are malicious as well, including fake crypto-currency investment schemes and other online scams.'
    },
    {
        name: 'Promotional Spammer (Products)',
        description: 'This account is most likely being used to spam promotions regarding products for sale on sites such as Amazon. Many of these products are either fake, misleading, or produced in an unethical manner.'
    },
    {
        name: 'Traditional Spam Account',
        description: 'This account is most likely being used to spam content regarding malicious activity, such as fake job offers and scam URLs. The majority of scam accounts on major platforms today would fall under this category.'
    },
    {
        name: 'Genuine User',
        description: 'This account is most likely human-operated, and does not seem to be engaging in any fraudulent or misleading activities. However, you should still be cautious when engaging with this account, especially if the risk meter is high.'
    },
    {
        name: 'Unknown',
        description: 'Due to lack of data, we are unable to determine what type of user this account is associated with. Please proceed with caution when engaging with this account.'
    }
]

const csvToTypeName = {
    'fake_followers_tweets.csv': 'Fake Follower',
    'social_spambots_1_tweets.csv': 'Political Spammer',
    'social_spambots_2_tweets.csv': 'Promotional Spammer (Apps/Services)',
    'social_spambots_3_tweets.csv': 'Promotional Spammer (Products)',
    'traditional_spambots_1_tweets.csv': 'Traditional Spam Account',
    'genuine_accounts_tweets.csv': 'Genuine User',
    'unknown': 'Unknown'
}

export function getScamType(csv) {
    let typeName = csvToTypeName[csv]
    return types.filter(t => t.name==typeName)[0]
}