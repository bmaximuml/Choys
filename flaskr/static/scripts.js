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
    document.querySelector(
        'div#filter-modal.modal > div.modal-content > div.modal-sliders'
    ).classList.remove('is-hidden');
}

function hideFilterModalSliders() {
    document.querySelector(
        'div#filter-modal.modal > div.modal-content > div.modal-sliders'
    ).classList.add('is-hidden');
}

function showFilterModalLoading() {
    document.querySelector(
        'div#filter-modal.modal > div.modal-content > div.modal-loading'
    ).classList.remove('is-hidden');
}

function hideFilterModalLoading() {
    document.querySelector(
        'div#filter-modal.modal > div.modal-content > div.modal-loading'
    ).classList.add('is-hidden');
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

// Add an event listener on the given element to filter the cards
function addEventFilterCards(element) {
    element.addEventListener('click', () => hideFilterModal());
}

// Hides filter modal on click of element which is a descendent of the specified id, and is of the specified class.
function idClassAddEventFilterCards(idName, className) {
    Array.from(document.getElementById(idName).getElementsByClassName(className)).forEach(item => addEventFilterCards(item));
}

// Hides filter modal on click of element of specified class which is a descendent of any of the specified ids, and is of any of the specified classes.
function idsClassesAddEventFilterCards(idNames, classNames) {
    idNames.forEach(idName => classNames.forEach(className => idClassAddEventFilterCards(idName, className)));
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

// Returns value of a slider for a given category
function getSliderValueForCategory(category) {
    const slider = document.getElementById(category + '_range');
    if (slider)
        return slider.value;
}


document.addEventListener("DOMContentLoaded", function(event) {
    document.getElementById('sorters').addEventListener('mousedown', function (e) {
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

    document.getElementById('sorters').addEventListener('mouseup', function (e) {
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
    document.getElementById('table-cards-btn').addEventListener('click', function (e) {
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
    document.getElementById('filter-btn').addEventListener('click', function() {
        showFilterModal();
    });

    const sliders = document.querySelectorAll('input[type="range"].slider');
    const outputs = document.querySelectorAll('input[type="number"].slider-output');

    idsClassesAddEventFilterCards(['filter-modal'], ['filter-modal-close', 'modal-close', 'modal-background']);
    addEventListenerSliders(sliders);
    addEventListenerSliderOutputs(outputs);
    updateAllModalSliderOutputs();
});
