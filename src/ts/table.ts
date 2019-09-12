class SortTable {
    tableID: string;
    table: HTMLTableElement;

    constructor(tableID: string) {
        this.tableID = tableID;
        this.table = null;
        this.initialise();
    }

    initialise() {
        this.table = <HTMLTableElement>document.getElementById(this.tableID);
        let headings: HTMLCollectionOf<HTMLTableHeaderCellElement> = this.table.getElementsByTagName('th');
        let tableIdentifier: string = this.tableID;
        let sortFunction: Function = this.sortColumnTable;
        for (let i: number = 0; i < headings.length; i++) {
            const heading: HTMLTableHeaderCellElement = headings[i];
            heading.onclick = function() {
                sortFunction(tableIdentifier, i);
            }
        }
    }

    /**
     * Sorts a table column
     * @param  {string} tableID
     */
    sortColumnTable(tableID: string, columnID: number) {
        let table: any;
        let rows: HTMLCollectionOf<HTMLTableRowElement>;
        let switching: Boolean = true;
        let shouldSwitch: Boolean
        let switchCount: number = 0;
        let direction: string = "ascending";
        let i: number, x: Element, y: Element;
        table = <HTMLTableElement>document.getElementById(tableID);
        switching = true;
        while (switching) {
          switching = false;
          rows = table.rows;
          for (i = 1; i < (rows.length - 1); i++) {
            shouldSwitch = false;
            x = rows[i].getElementsByTagName("TD")[columnID];
            y = rows[i + 1].getElementsByTagName("TD")[columnID];
            if (direction == "ascending") {
                if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                  shouldSwitch = true;
                  break;
                }
            } else if (direction == "descending") {
                if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                  shouldSwitch = true;
                  break;
                }
            }
          }
          if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            switchCount++;
          } else {
              if (switchCount == 0 && direction == "ascending") {
                  direction = "descending";
                  switching = true;
              }
          }
        }
    }
}


export {
    SortTable
}