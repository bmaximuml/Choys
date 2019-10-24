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

document.addEventListener('mousedown', function (e) {
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

document.addEventListener('mouseup', function (e) {
    let table = document.getElementById("compare_table");
    let rows = table.rows;
    heapSortGeneric(mouse_down_sort_by, table, rows, {header_row: table.rows[0]});

    let cards_div = document.getElementById('cards');
    let cards = [];
    for (const card_row of cards_div.children) {
        for (const card of card_row.children) {
            cards.push(card);
        }
    }
    heapSortGeneric(mouse_down_sort_by, cards_div, cards, {columns: 5});

    updateColours();

    let sorters = document.getElementsByClassName("sort_btn");
    for (const sorter of sorters) {
        sorter.classList.remove('is-loading');
    }
}, false);

// Card / Table switcher button
document.addEventListener('click', function (e) {
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

if (table_cards === 'table') {
}
else if (table_cards === 'cards') {
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

function updateColours() {
    let cards = document.getElementById('cards');
    let colour = 'is-link';
    for (const row of cards.children) {
        for (const card of row.children) {
            if (!card.classList.contains(colour)) {
                card.classList.remove((colour === 'is-link') ? 'is-dark' : 'is-link');
                card.classList.add(colour);
            }
            colour = (colour === 'is-link') ? 'is-dark' : 'is-link';
        }
    }
}
