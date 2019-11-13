import {Selector} from 'testcafe';

fixture `Getting Started`
    .page `https://jupyter.clue.io`;


const cell = Selector('a').withExactText("Cell");
const runAll = Selector('a').withExactText("Run All");
var urlstartswith = new RegExp('^data:image/png;base64,iVBOR');

test("jupyter user", async t => {
    const index =  process.argv[4];
    const name = "foo_" + index;
    console.log("User: " + name + " Browser: " + process.argv[2]);
    await t
        .typeText('#username_input', name)
        .typeText('#password_input', 'wat')
        .click('#login_submit');
    await t
        .click(Selector('span').withExactText("workshop"));
    await t
        .click(Selector('span').withExactText("Module4"));
    await t
        .click(Selector('span').withExactText("cross_cell_example_R.ipynb"));
    const cellElement = await cell();
    await t
        .click(cellElement);
    const runAllElement = await runAll();
    await t
        .click(runAllElement);
    await t
        .expect(Selector('img').withAttribute("src", urlstartswith)).ok();
});