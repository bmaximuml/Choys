let last_sort_by = 7;
let last_sort_dir = 'asc';
let mouse_down_sort_by = 7;

let table_cards = 'table';

function heapifyTable(arr, n, i, sort_by, dir) {
    // Find largest among root and children
    let largest = i;
    let left = 2 * i + 1;
    let right = 2 * i + 2;

    if (left < n) {
        let arr_i, arr_left, i_comp, left_comp;
        arr_i = getItem(arr, i, sort_by);
        arr_left = getItem(arr, left, sort_by);

        i_comp = getDataValue(arr_i);
        left_comp = getDataValue(arr_left);

        if (dir === 'asc') {
            if (i_comp < left_comp) {
                largest = left;
            }
        }
        else { // dir === 'desc'
            if (i_comp > left_comp) {
                largest = left;
            }
        }
    }

    if (right < n) {
        let arr_largest, arr_right, largest_comp, right_comp;
        arr_largest = getItem(arr, largest, sort_by);
        arr_right = getItem(arr, right, sort_by);

        largest_comp = getDataValue(arr_largest);
        right_comp = getDataValue(arr_right);
        if (dir === 'asc') {
            if (largest_comp < right_comp) {
                largest = right;
            }
        }
        else { // dir === 'desc'
            if (largest_comp > right_comp) {
                largest = right;
            }
        }
    }

    // If root is not largest, swap with largest and continue heapifying
    if (largest !== i) {
        let tmp = arr[largest];
        arr[largest] = arr[i];
        arr[i] = tmp;
        heapifyTable(arr, n, largest, sort_by, dir);
    }
}

function heapSortGeneric(sort_by, wrapper, items, opts) {
    let i;

    let arr = (opts.header_row) ? Array.prototype.slice.call(items).slice(1) :
        Array.prototype.slice.call(items);
    let n = arr.length;

    // Build max heap
    for (i = n - 1; i >= 0; i--) {
        if (last_sort_by === sort_by && last_sort_dir === 'asc') {
            heapifyTable(arr, n, i, sort_by, 'desc');
        }
        else {
            heapifyTable(arr, n, i, sort_by, 'asc');
        }
    }

    for (i = n - 1; i >= 0; i--) {
        // swap
        let tmp = arr[i];
        arr[i] = arr[0];
        arr[0] = tmp;

        // heapify root element

        if (last_sort_by === sort_by && last_sort_dir === 'asc') {
            heapifyTable(arr, i, 0, sort_by, 'desc');
        }
        else {
            heapifyTable(arr, i, 0, sort_by, 'asc');
        }

    }
    while (wrapper.firstChild) {
        wrapper.removeChild(wrapper.firstChild);
    }
    if (opts.header_row) {
        wrapper.appendChild(opts.header_row);
    }

    if (opts.columns && opts.columns > 1) {
        let columns, j;
        for (i = 0; i < Math.ceil(n / opts.columns); i++) {
            columns = document.createElement('div');
            columns.classList.add('columns');
            for (j = 0; j < opts.columns && (i * opts.columns) + j < n; j++) {
                columns.appendChild(arr[(i * opts.columns) + j]);
            }
            wrapper.appendChild(columns);
        }
    }
    else {
        for (i = 0; i < n; i++) {
            wrapper.appendChild(arr[i]);
        }
    }
}

// Return an HTMLCollection of all cards
function getAllCards() {
    const grandparent = document.getElementById('cards');
    if (grandparent && grandparent.hasChildNodes()) {
        const parent = grandparent.firstElementChild;
        if (parent && parent.hasChildNodes())
            return parent.childNodes;
    }
}

function getTarget(e, parent = '', child = '', grandchild = '') {
    e = e || Event;
    let target = e.target || Event.target;

    if (target.tagName === parent) {
        target = target.firstElementChild;
    }
    else if (target.tagName === child) {
        target = target.parentElement;
    }
    else if (target.tagName === grandchild) {
        target = target.parentElement.parentElement;
    }

    return target;
}

function getItem(arr, num, sort_by) {
    let result;
    if (arr[num].cells) {
        result = arr[num].cells[sort_by];
    }
    if (!result) {
        result = arr[num].children[sort_by]
    }
    return result;
}

function getDataValue(item) {
    let attr = item.getAttribute('data-value');
    if (isNaN(attr)) {
        return attr;
    }
    else {
        return +attr;
    }
}

// Return true if an element is current shown (not hidden), false otherwise
function isShown(element) {
    return element.classList && !(element.classList.contains('is-hidden'))
}

// Return true if an element is current hidden false otherwise
function isHidden(element) {
    return element.classList && (element.classList.contains('is-hidden'))
}

function hide(element) {
    if (isShown(element)) {
        element.classList.add('is-hidden');
    }
}

function show(element) {
    if (isHidden(element)) {
        element.classList.remove('is-hidden');
    }
}

function updateColours() {
    const cards = document.getElementById('cards').firstElementChild;
    const colours = ['is-link', 'is-success', 'is-primary', 'is-warning', 'is-danger', 'is-dark'];
    let colour = 0;
    for (const card of cards.children) {
        if (isShown(card)) {
            if (!card.classList.contains(colours[colour])) {
                for (const rm_colour of colours) {
                    card.classList.remove(rm_colour);
                }
                card.classList.add(colours[colour]);
            }
            colour = (colour === colours.length - 1) ? 0 : colour + 1;
        }
    }
}

function showFilterModal() {
    document.getElementById('filter-modal').classList.add('is-active');
}

function hideFilterModal() {
    document.getElementById('filter-modal').classList.remove('is-active');
    hideFilterModalLoading();
    showFilterModalSliders();
}

function showFilterModalSliders() {
    show(document.querySelector(
        'div#filter-modal.modal > div.modal-content > div.modal-sliders'
    ));
}

function hideFilterModalSliders() {
    hide(document.querySelector(
        'div#filter-modal.modal > div.modal-content > div.modal-sliders'
    ));
}

function showFilterModalLoading() {
    show(document.querySelector(
        'div#filter-modal.modal > div.modal-content > div.modal-loading'
    ));
}

function hideFilterModalLoading() {
    hide(document.querySelector(
        'div#filter-modal.modal > div.modal-content > div.modal-loading'
    ));
}

function setElementMaxValue(element) {
    element.value = element.max;
}

// Find output element associated to the DOM element passed as parameter
// Assumes there is only one output for the given element
// If there is more than one output element, will return the last one in the DOM
function findOutputForSlider(element) {
    let result = null;
    document.querySelectorAll('input[type=number].slider-output').forEach(output => {
        if (output.dataset.for === element.id) {
            result = output;
        }
    });
    return result;
}

// Find slider element associated to the DOM element passed as parameter
// Assumes there is only one slider for the given element
// If there is more than one slider element, will return the last one in the DOM
function findSliderForOutput(element) {
    let result = null;
    document.querySelectorAll('input[type=range].slider').forEach(slider => {
        if (slider.id === element.dataset.for) {
            result = slider;
        }
    });
    return result;
}

function getAllSliders() {
    return document.querySelectorAll('input[type=range].slider');
}

function getAllSliderOutputs() {
    return document.querySelectorAll('input[type=number].slider-output');
}

function getAllSwitches() {
    return document.querySelectorAll('select.slider-switch');
}

function getAllRows() {
    return document.querySelectorAll('table#compare_table tr');
}

function updateModalSlider(output) {
    const slider = findSliderForOutput(output);
    if (slider)
        slider.value = output.value;
}

function updateModalSliderOutput(slider) {
    const output = findOutputForSlider(slider);
    if (output)
        output.value = Math.round(slider.value);
}

function updateAllModalSliderOutputs() {
    const sliders = document.querySelectorAll('input[type="range"].slider');
    sliders.forEach(slider => updateModalSliderOutput(slider));
}

function addEventListenerSlider(slider) {
    slider.addEventListener('mousemove', () => updateModalSliderOutput(slider));
    slider.addEventListener('change', () => updateModalSliderOutput(slider));
}

function addEventListenerSliders(sliders) {
    sliders.forEach(slider => addEventListenerSlider(slider));
}

function addEventListenerSliderOutput(output) {
    output.addEventListener('change', () => updateModalSlider(output));
}

function addEventListenerSliderOutputs(outputs) {
    outputs.forEach(output => addEventListenerSliderOutput(output));
}

// Add an event listener on click of the given element to filter the cards
function addEventFilter(element) {
    element.addEventListener('mousedown', () => startFiltering());
    element.addEventListener('mouseup', () => filterCards());
    element.addEventListener('mouseup', () => filterTable());
}

// Add an event listener on click of descendents of the given class to filter the cards
function addEventsFilter(className) {
    Array.from(document.getElementsByClassName(className)).forEach(item => addEventFilter(item));
}

// Add an event listener on click of the given element to reset the filters
function addEventReset(element) {
    element.addEventListener('click', () => resetFilters());
}

// Add an event listener on click of descendents of the given class to reset the filters
function addEventsReset(className) {
    Array.from(document.getElementsByClassName(className)).forEach(item => addEventReset(item));
}

// Returns value of a particular category for a given element
// Will perform a recursive DFS of element's children until a value is found
// If multiple children exist, will return the value for the first one found
function getCategoryValueForElement(element, category) {
    let result = null;
    if (element.classList && element.dataset.category === category)
        return element.dataset.value;
    if (element.hasChildNodes() > 0) {
        element.childNodes.forEach(child => {
            const child_result =  getCategoryValueForElement(child, category);
            if (child_result)
                result = child_result
        });
    }
    return result;
}

function startFiltering() {
    showFilterModal();
    hideFilterModalSliders();
    showFilterModalLoading();
}

function filter(data, element_type) {
    const all_sliders = getAllSliders();
    const all_switches = getAllSwitches();

    data.forEach(element => {
        all_sliders.forEach((slider, i) => {
            if (element.nodeName === element_type) {
                const element_value = getCategoryValueForElement(element, slider.dataset.category);
                if ((all_switches[i].value === 'or-more' && element_value < slider.value)
                        || (all_switches[i].value === 'or-less' && element_value > slider.value))
                    hide(element);
                else
                    show(element);
            }
        });
    });

    updateColours();
    hideFilterModal();
}

function filterCards() {
    filter(getAllCards(), 'DIV');
}

function filterTable() {
    filter(getAllRows(), 'TR');
}

function resetFilters() {
    getAllSliders().forEach(slider => setElementMaxValue(slider));
    getAllSliderOutputs().forEach(output => setElementMaxValue(output));

    getAllCards().forEach(card => show(card));
    getAllRows().forEach(row => show(row));

    updateColours();
    hideFilterModal();
}

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById('sorters').addEventListener('mousedown', (e) => {
        let target = getTarget(e, 'DIV', 'SPAN', 'I');

        if (target.classList.contains('sort_btn')) {
            mouse_down_sort_by = parseInt(target.getAttribute('data-sort'));
            last_sort_dir = (last_sort_by === mouse_down_sort_by && last_sort_dir === 'asc' ? 'desc' : 'asc');
            last_sort_by = mouse_down_sort_by;

            let sort_btns = document.getElementsByClassName('sort_btn');
            for (const btn of sort_btns) {
                btn.classList.remove('is-selected');
                btn.classList.remove('is-primary');
                btn.classList.remove('is-danger');

                btn.children[0].children[0].classList.remove('fa-chevron-up');
                btn.children[0].children[0].classList.remove('fa-chevron-down');
                btn.children[0].children[0].classList.remove('fa-chevron-right');
                btn.children[0].children[0].classList.add('fa-chevron-right');
            }
            target.children[0].children[0].classList.remove('fa-chevron-right');
            if (last_sort_dir === 'asc') {
                target.classList.add('is-primary');
                target.children[0].children[0].classList.add('fa-chevron-down');
            } else {
                target.classList.add('is-danger');
                target.children[0].children[0].classList.add('fa-chevron-up');
            }
            target.classList.add('is-selected');
            target.classList.add('is-loading');
        }
    }, false);

    document.getElementById('sorters').addEventListener('mouseup', () => {
        let table = document.getElementById("compare_table");
        let rows = table.rows;
        heapSortGeneric(mouse_down_sort_by, table, rows, {header_row: table.rows[0]});

        let cards_div = document.getElementById('cards').firstElementChild;
        heapSortGeneric(mouse_down_sort_by, cards_div, cards_div.children, {});

        updateColours();

        let sorters = document.getElementsByClassName("sort_btn");
        for (const sorter of sorters) {
            sorter.classList.remove('is-loading');
        }
    }, false);

    // Card / Table switcher button
    document.getElementById('table-cards-btn').addEventListener('click', (e) => {
        let target = getTarget(e, '', 'SPAN', 'I');

        let grandchild = target.children[0].children[0];

        let first_colour = 'is-danger';
        let second_colour = 'is-link';
        let first_fa = 'fa-list-alt';
        let first_fa_short = 'far';
        let second_fa = 'fa-th';
        let second_fa_short = 'fas';

        if (target.id === 'table-cards-btn') {
            if (target.classList.contains(first_colour)) {
                target.classList.remove(first_colour);
                target.classList.add(second_colour);

                grandchild.classList.remove(first_fa);
                grandchild.classList.remove(first_fa_short);
                grandchild.classList.add(second_fa);
                grandchild.classList.add(second_fa_short);

                document.getElementById('compare_table').style.display = 'table';
                document.getElementById('compare_cards').style.display = 'none';
            }
            else {
                target.classList.remove(second_colour);
                target.classList.add(first_colour);

                grandchild.classList.remove(second_fa);
                grandchild.classList.remove(second_fa_short);
                grandchild.classList.add(first_fa);
                grandchild.classList.add(first_fa_short);

                document.getElementById('compare_table').style.display = 'none';
                document.getElementById('compare_cards').style.display = 'block';
            }
        }
    }, false);

    // Show filter modal on button click
    document.getElementById('filter-btn').addEventListener('click', () => {
        showFilterModal();
    });

    const sliders = document.querySelectorAll('input[type="range"].slider');
    const outputs = document.querySelectorAll('input[type="number"].slider-output');

    addEventsFilter('filter-modal-close');
    addEventsFilter('modal-loading');
    addEventsReset('filter-modal-reset');
    addEventListenerSliders(sliders);
    addEventListenerSliderOutputs(outputs);
    updateAllModalSliderOutputs();
    filterCards();
    filterTable();
});
