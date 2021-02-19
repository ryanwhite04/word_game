function getWords(url) {
    console.log('getWords', url);
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
    return [...actual].reduce((matches, letter, i) => {
        letter == guess[i] && matches.push(i)
        return matches;
    }, []).length;
}

main(8, 4).then(console.log).catch(console.error);

const template = document.createElement('template');

getWords(new URL('diceware.wordlist.asc.txt', import.meta.url).href).then(words => {
    customElements.define('word-game', class extends HTMLElement {
        
        static get observedAttributes() {
            return ['options', 'guesses', 'length'];
        }

        static get html() {
            const template = document.createElement('template');
            template.innerHTML = `
                <p>bla</p>
                <ol id="choices"></ol>
            `;
            return template;
        }
        constructor() {
            super();
            this.words = words
            const root = this.attachShadow({ mode: 'open' });
            const style = document.createElement('style');
            style.textContent = `
                #choices input[type="button"] {
                    width: 100px;
                    margin: 5px;
                }
                #choices input[type="button"][correct] {
                    background: green;
                }
            `;
            this.shadowRoot.append(style); // can accept any other elements too
            this.shadowRoot.appendChild(this.constructor.html.content.cloneNode(true))
            console.log(this, this.options, this.guesses);
        }

        displayChoices() {
            console.log('displayChoices')
            const list = this.shadowRoot.getElementById('choices');
            list.innerHTML = '';
            const items = this.choices.reduce((items, choice) => {
                const button = document.createElement('input');
                button.value = choice;
                button.setAttribute('type', 'button');
                button.addEventListener('click', this.selectChoice(choice));
                const item = document.createElement('li');
                item.appendChild(button);
                if (this.chosen.hasOwnProperty(choice)) {
                    let score = document.createElement('span');
                    if (choice === this.answer) {
                        button.setAttribute('correct', true);
                        score.textContent = "Correct!";
                    } else {
                        button.setAttribute('disabled', true);
                        score.textContent = this.chosen[choice] + " Matching Letter";
                    }
                    item.appendChild(score);
                }
                items.appendChild(item);
                return items;
            }, document.createDocumentFragment());
            list.appendChild(items);
            if (!this.remaining) {
                let message = document.createElement('span');
                message.textContent = 'Game Over';
                list.appendChild(message);
            }
        }

        selectChoice(choice) {
            return e => {
                console.log(choice, e, this);
                this.chosen[choice] = matchWords(choice, this.answer);
                this.remaining--;
                this.displayChoices();
            }
        }

        set length(value) {
            this.setAttribute('length', value);
        }

        get length() {
            return parseInt(this.getAttribute('length'));
        }

        set options(value) {
            this.setAttribute('options', value);
        }

        get options() {
            return parseInt(this.getAttribute('options'));
        }

        set guesses(value) {
            this.setAttribute('guesses', value);
        }

        get guesses() {
            return parseInt(this.getAttribute('guesses'));
        }

        choose() {
            let filtered = words.filter(word => word.length == this.length);
            let choices = getChoices(filtered, this.options);
            this.answer = choices[~~(Math.random() * choices.length)];
            this.chosen = {};
            return choices;
        }

        connectedCallback() {
            console.log('word-game', 'connected', this);
        }

        disconnectedCallback() {
            console.log('word-game', 'disconnected', this);
        }

        adoptedCallback() {
            console.log('word-game', 'adopted', this);
        }

        attributeChangedCallback(name, oldValue, newValue) {
            console.log('word-game', 'attributeChanged', { name, oldValue, newValue });
            this.choices = this.choose();
            this.remaining = this.guesses;
            this.displayChoices();
        }
    })
}).catch(console.error)

