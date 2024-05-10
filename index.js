const button = document.querySelector('#butt-1');
const button2 = document.querySelector('#butt-2');
const button3 = document.querySelector('#butt-3');
let display = document.querySelector('#my-area');
let Hblocks = document.querySelector('#history-blocks');
const answer = document.querySelector('#answer-own');
let text_in = null;
const versions = ['class-for-historic-block2-v-1', 'class-for-historic-block2-v-2', 'class-for-historic-block2-v-3'];
// pos = '<svg width="24px" height="24px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"> <circle cx="12" cy="12" r="10" stroke="#000000" stroke-width="2" stroke-linecap="round"/><path d="M8 9.05001V8.95001" stroke="#000000" stroke-width="2" stroke-linecap="round"/><path d="M16 9.05001V8.95001" stroke="#000000" stroke-width="2" stroke-linecap="round"/><path d="M16 14C15.5 15.5 14.2091 17 12 17C9.79086 17 8.5 15.5 8 14" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>';

// const reactions = ['Neutral', 'Negative', 'Positive'];



display.addEventListener('change', () =>{ 
  text_in = display.value;
})

button.addEventListener('click', async function () {
  
    console.log('Click!');
    console.log(text_in);
    display.focus();

    
    const response = await fetch(
      "https://kruase.serveo.net/api",
      {
          method: "POST",
          body: JSON.stringify({text: text_in}),
          headers: {
              "Content-Type": "application/json",
              "Accept": "application/json"
          }
      }
    );

    const sentiment = (await response.json()).sentiment;



    button2.addEventListener('click', function () {
      display.value = '';
    })

    answer.classList.remove('answer-own-1');
    answer.classList.remove('answer-own-2');
    answer.classList.remove('answer-own-3');

    if (sentiment == "neutral") {
      answer.classList.add('answer-own-1');
    }
    else if (sentiment == "negative") {
      answer.classList.add('answer-own-2');
    }
    else if (sentiment == "positive") {
      answer.classList.add('answer-own-3');
    }

    // answer.innerHTML = pos;
    answer.innerText = sentiment;

    const block = document.createElement('div');
    block.classList.add('class-for-global-historic');
    
    const block1 = document.createElement('div');
    block1.style['padding'] = '5px';
    block1.innerText = text_in;

    const block2 = document.createElement('div');
    if (sentiment == "neutral") {
      block2.classList.add(versions[0]);
    }
    else if (sentiment == "negative") {
      block2.classList.add(versions[1]);
    }
    else if (sentiment == "positive") {
      block2.classList.add(versions[2]);
    }
    block2.innerText = sentiment;
    
    Hblocks.insertBefore(block, Hblocks.children[0]);
    block.append(block1);
    block.append(block2);

    button3.addEventListener('click', function () {
      block.remove();
    })

    display.focus();

    // const block = `<div>${text_in}</div>`;
    // block.classList.add('class-for-historic');
    // Hblocks.insertAdjacentHTML('beforeend', block);
  

})