function getWords(url) {
    return fetch(url)
        .then(body => body.text())
        .then(text => text.split('\n').slice(2, 6**5 + 2).map(line => line.split('\t')[1]))
}

function getChoices(options, count) {
    return [...new Array(count)].map(i => options.splice(~~(options.length*Math.random()), 1)[0]);
}
async function main(words, guesses) {
    const options = await getWords('diceware.wordlist.asc.txt')
        .then(list => list.filter(word => word.length == 6))
        .catch(console.error);
    const choices = getChoices(options, words);
    const correct = choices[~~(Math.random()*choices.length)];
    console.log('Select from the following: ', choices, correct);
    let question = (answer) => {
        if (guesses--) {
            return matchWords(correct, choices[answer - 1]);
        } else {
            console.log('game over');
        }
    }
    return question;
}

function matchWords(actual, guess) {
    const matches = [...actual].reduce((matches, letter, i) => {
        letter == guess[i] && matches.push(i)
        return matches;
    }, [])
    return `${matches.length}/${actual.length}`;
}

main(8, 4).then(console.log).catch(console.error);
