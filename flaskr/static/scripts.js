let last_sort_by = -1;
let last_sort_dir = 'asc';

function bubbleSortTable(sort_by) {
    let table, rows, switching, i, x, y, x_comp, y_comp, shouldSwitch, dir, switchcount = 0;
    table = document.getElementById("compare_table");
    switching = true;
    // Set the sorting direction to ascending
    dir = 'asc';
    // Make a loop that will continue until no switching has been done:
    while (switching) {
        // start by saying no switching is done:
        switching = false;
        rows = table.rows;
        // Loop through all table rows (except the first which is headers)
        for (i = 1; i < (rows.length - 1); i++) {
            // start by saying there should by no switching
            shouldSwitch = false;
            // Get the two elements you want to compare, one from current row and one from next
            x = rows[i].getElementsByTagName('td')[sort_by];
            y = rows[i + 1].getElementsByTagName('td')[sort_by];
            // Check if the values are numeric or strings
            if (isNaN(x.innerHTML) || isNaN(y.innerHTML)) {
                x_comp = x.innerHTML.toLowerCase();
                y_comp = y.innerHTML.toLowerCase();
            }
            else {
                x_comp = +x.innerHTML;
                y_comp = +y.innerHTML;
            }
            // Check if the two rows should switch place, based on the direction, asc or desc
            if (dir === 'asc') {
                if (x_comp > y_comp) {
                    // if so, mark as a switch and break the loop
                    shouldSwitch = true;
                    break;
                }
            } else if (dir === 'desc') {
                if (x_comp < y_comp) {
                    // if so, mark as a switch and break the loop
                    shouldSwitch = true;
                    break;
                }
            }
        }
        if (shouldSwitch) {
            // If a switch has been marked, make the switch and mark that a switch has been done
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            switchcount++;
        } else {
            // If no switching has been done AND the direction is 'asc', set the direction to 'desc' and run the while
            // loop again
            if (switchcount === 0 && dir === 'asc') {
                dir = 'desc';
                switching = true;
            }
        }
    }
}

function heapify(arr, n, i) {
    // Find largest among root and children
    let largest = i;
    let left = 2 * i + 1;
    let right = 2 * i + 2;

    if (left < n && arr[i] < arr[left]) {
        largest = left;
    }

    if (right < n && arr[largest] < arr[right]) {
        largest = right;
    }

    // If root is not largest, swap with largest and continue heapifying
    if (largest !== i) {
        let tmp = arr[largest];
        arr[largest] = arr[i];
        arr[i] = tmp;
        heapify(arr, n, largest);
    }
}

function heapifyTable(arr, n, i, sort_by, dir) {
    // Find largest among root and children
    let largest = i;
    let left = 2 * i + 1;
    let right = 2 * i + 2;

    if (left < n) {
        let arr_i, arr_left, i_comp, left_comp;
        arr_i = arr[i].getElementsByTagName('td')[sort_by];
        arr_left = arr[left].getElementsByTagName('td')[sort_by];

        if (isNaN(arr_i.innerHTML) || isNaN(arr_left.innerHTML)) {
            i_comp = arr_i.innerHTML.toLowerCase();
            left_comp = arr_left.innerHTML.toLowerCase();
        } else {
            i_comp = +arr_i.innerHTML;
            left_comp = +arr_left.innerHTML;
        }
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
        arr_largest = arr[largest].getElementsByTagName('td')[sort_by];
        arr_right = arr[right].getElementsByTagName('td')[sort_by];

        if (isNaN(arr_largest.innerHTML) || isNaN(arr_right.innerHTML)) {
            largest_comp = arr_largest.innerHTML.toLowerCase();
            right_comp = arr_right.innerHTML.toLowerCase();
        } else {
            largest_comp = +arr_largest.innerHTML;
            right_comp = +arr_right.innerHTML;
        }
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

function heapSort(arr) {
    let n = arr.length;

    // Build max heap
    for (let i = n; i >= 0; i--) {
        heapify(arr, n, i);
    }

    for (let i = n - 1; i >= 0; i--) {
        // swap
        let tmp = arr[i];
        arr[i] = arr[0];
        arr[0] = tmp;

        // heapify root element
        heapify(arr, i, 0);
    }
}

function heapSortTable(sort_by) {
    let i;
    let table = document.getElementById("compare_table");
    let rows = table.rows;
    // -1 to account for header row
    let n = rows.length - 1;
    // Convert HTMLCollection to array, then remove header row (i.e. slice first row)
    let arr = Array.prototype.slice.call(rows).slice(1);
    // let arr = rows.slice(1);

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
    let header_row = table.rows[0];
    while (table.firstChild) {
        table.removeChild(table.firstChild);
    }
    table.appendChild(header_row);
    for (i = 0; i < n; i++) {
        // table.append(arr);
        table.appendChild(arr[i]);
    }
}

function sortTable(sort_by) {
    // console.log('last_sort_dir: ' + last_sort_dir);
    // console.log('last_sort_by: ' + last_sort_by);
    // bubbleSortTable(sort_by);
    heapSortTable(sort_by);
    last_sort_dir = (last_sort_by === sort_by && last_sort_dir === 'asc' ? 'desc' : 'asc')
    last_sort_by = sort_by;
}

function w3cBubbleSortTable(sort_by) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById("compare_table");
  switching = true;
  //Set the sorting direction to ascending:
  dir = "asc";
  //Make a loop that will continue until no switching has been done:
  while (switching) {
    //start by saying: no switching is done:
    switching = false;
    rows = table.rows;
    // Loop through all table rows (except the first, which contains table headers):
    for (i = 1; i < (rows.length - 1); i++) {
      //start by saying there should be no switching:
      shouldSwitch = false;
      // Get the two elements you want to compare, one from current row and one from the next:
      x = rows[i].getElementsByTagName("TD")[sort_by];
      y = rows[i + 1].getElementsByTagName("TD")[sort_by];
      // check if the two rows should switch place, based on the direction, asc or desc:
      if (dir == "asc") {
        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
          //if so, mark as a switch and break the loop:
          shouldSwitch= true;
          break;
        }
      } else if (dir == "desc") {
        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
          //if so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      }
    }
    if (shouldSwitch) {
      // If a switch has been marked, make the switch and mark that a switch has been done:
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      //Each time a switch is done, increase this count by 1:
      switchcount ++;
    } else {
      //If no switching has been done AND the direction is "asc", set the direction to "desc" and run the while loop again.
      if (switchcount == 0 && dir == "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
}