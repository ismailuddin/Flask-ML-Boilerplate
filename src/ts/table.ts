class SortTable {
    tableID: string;
    table: HTMLTableElement;
    direction: ObjectConstructor

    constructor(tableID: string) {
        this.tableID = tableID;
        this.table = null;
        this.setIconsForHeader();
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
    
    setIconsForHeader() {
        let table = <HTMLTableElement>document.getElementById(this.tableID);
        let headers: HTMLCollectionOf<HTMLTableHeaderCellElement>;
        headers = table.getElementsByTagName("th");
        for (let i: number = 0; i < headers.length; i++) {
            let header = <HTMLTableHeaderCellElement>headers[i];
            header.classList.add("random");
        }
        
    }

    /**
     * Sorts a table column
     * @param  {string} tableID
     * @param  {number} columnID
     */
    sortColumnTable = (tableID: string, columnID: number) => {
        let table: any;
        let rows: HTMLCollectionOf<HTMLTableRowElement>;
        let switching: Boolean = true;
        let shouldSwitch: Boolean
        let switchCount: number = 0;
        let direction: string = "ascending";
        let i: number, x: Element, y: Element;
        table = <HTMLTableElement>document.getElementById(tableID);
        rows = table.rows;
        let columnIsNumeric: boolean = this.checkColumnType(rows, columnID);
        /**
         * Perform sort on table
         */
        switching = true;
        while (switching) {
          switching = false;
          rows = table.rows;
          for (i = 1; i < (rows.length - 1); i++) {
            shouldSwitch = false;
            x = rows[i].getElementsByTagName("TD")[columnID];
            y = rows[i + 1].getElementsByTagName("TD")[columnID];
            let firstVal: any, secondVal: any;
            if (columnIsNumeric){
                firstVal = Number(x.innerHTML);
                secondVal = Number(y.innerHTML);
            } else {
                firstVal = x.innerHTML.toLowerCase();
                secondVal = y.innerHTML.toLowerCase();
            }
            if (direction == "ascending") {
                if (firstVal > secondVal) {
                  shouldSwitch = true;
                  break;
                }
            } else if (direction == "descending") {
                if (firstVal < secondVal) {
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

        /**
         * Apply CSS styling to header row; show icons
         */
        let header = table.getElementsByTagName("th")[columnID];
        if (direction == "ascending") {
            header.classList.remove("random");
            header.classList.remove("desc");
            header.classList.add("asc");
        } else {
            header.classList.remove("random");
            header.classList.remove("asc");
            header.classList.add("desc");

        }
    }

    isNumeric(inputString: string){
        return !isNaN(inputString as any)
    }

    checkColumnType(
        rows: HTMLCollectionOf<HTMLTableRowElement>,
        id: number
    ): boolean {
        for (let i = 1; i < rows.length; i++) {
            let cell: HTMLTableCellElement = rows[i].getElementsByTagName('td')[id];
            if (!this.isNumeric(cell.innerText)) {
                return false;
            }
        }
        return true;
    }
}


export {
    SortTable
}