const button = document.querySelector('#butt-1');
const button2 = document.querySelector('#butt-2');
const button3 = document.querySelector('#butt-3');
let display = document.querySelector('#my-area');
let Hblocks = document.querySelector('#history-blocks');
const answer = document.querySelector('#answer-own');
const versions = ['class-for-historic-block2-v-1', 'class-for-historic-block2-v-2', 'class-for-historic-block2-v-3'];

const timeout = 5;


button.onclick = async function() {
    display.focus();

    if (!display.value) return;

    const response = await fetch(
        "https://kruase.serveo.net/api",
        {
            method: "POST",
            body: JSON.stringify({text: display.value}),
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        }
    );
    const sentiment = (await response.json()).sentiment;

    answer.classList.remove('answer-own-1', 'answer-own-2', 'answer-own-3');

    if (sentiment == "neutral") {
        answer.classList.add('answer-own-1');
    } else if (sentiment == "negative") {
        answer.classList.add('answer-own-2');
    } else if (sentiment == "positive") {
        answer.classList.add('answer-own-3');
    }

    answer.innerText = sentiment;

    const block = document.createElement('div');
    block.classList.add('class-for-global-historic');

    const block1 = document.createElement('div');
    block1.style['padding'] = '5px';
    block1.innerText = display.value;

    const block2 = document.createElement('div');
    if (sentiment == "neutral") {
        block2.classList.add(versions[0]);
    } else if (sentiment == "negative") {
        block2.classList.add(versions[1]);
    } else if (sentiment == "positive") {
        block2.classList.add(versions[2]);
    }
    block2.innerText = sentiment;

    Hblocks.insertBefore(block, Hblocks.children[0]);
    block.append(block1);
    block.append(block2);

    display.focus();

    button.disabled = true;

    for (let time = 0; time <= timeout; time++) {
        setTimeout(
            function() {
                button.textContent = timeout - time;
            },
            time * 1000
        );
    }

    setTimeout(
        function() {
            button.textContent = "Проанализировать";
            button.disabled = false;
        },
        timeout * 1000
    );
}

button3.onclick = function() {
    block.remove();
}

button2.onclick = function() {
    display.value = '';
}
