$( document ).ready(function() {
    let docHeight = $("section").innerHeight();
    let viewportHeight = screen.height;
    let headerHeight = $(".header").height();    
    newHieght = viewportHeight - parseInt(275);
    newHieght = docHeight - headerHeight;
    document.getElementById("secRight").style.height = newHieght;
    document.getElementById("secLeft").style.height = newHieght;
});


class TableCsv {
  /**
   * @param {HTMLTableElement} root The table element which will display the CSV data.
   */
  constructor(root) {
    this.root = root;
  }

  /**
   * Clears existing data in the table and replaces it with new data.
   *
   * @param {string[][]} data A 2D array of data to be used as the table body
   * @param {string[]} headerColumns List of headings to be used
   */
  update(data, headerColumns = []) {
    this.clear();
    this.setHeader(headerColumns);
    this.setBody(data);
  }


  /**
   * Clears all contents of the table (incl. the header).
   */
  clear() {
    this.root.innerHTML = "";
  }

  /**
   * Sets the table header.
   *
   * @param {string[]} headerColumns List of headings to be used
   */
  setHeader(headerColumns) {
    this.root.insertAdjacentHTML(
      "afterbegin",
      `
            <thead id="head">
                <tr>
                    ${headerColumns.map((text) => `<th scope="col">${text}</th>`).join("")}
                </tr>
            </thead>
        `
    );
  }

  /**
   * Sets the table body.
   *
   * @param {string[][]} data A 2D array of data to be used as the table body
   */
  setBody(data) {
    const rowsHtml = data.map((row) => {
      return `
                <tr>
                    ${row.map((text) => `<td id="data">${text}</td>`).join("")}
                </tr>
            `;
    });

    this.root.insertAdjacentHTML(
      "beforeend",
      `
            <tbody>
                ${rowsHtml.join("")}
            </tbody>
        `
    );
  }
}
const csv1File = '{{ settings.MEDIA_URL }}{{ job }}/Table1.csv';
const csv1FileInput = csv1File.toString();
const table1Root = document.querySelector("#csv1Root");
const table1Csv = new TableCsv(table1Root);


Papa.parse(csv1File, {
  delimiter: ",",
  download: true,
  skipEmptyLines: true,
  complete: (results) => {
    table1Csv.update(results.data.slice(1), results.data[0]);
  }
});

const csv2File = '{{ settings.MEDIA_URL }}{{ job }}/Table2.csv';
const csv2FileInput = csv2File.toString();
const table2Root = document.querySelector("#csv2Root");
const table2Csv = new TableCsv(table2Root);


Papa.parse(csv2File, {
  delimiter: ",",
  download: true,
  skipEmptyLines: true,
  complete: (results) => {
    table2Csv.update(results.data.slice(1), results.data[0]);
  }
});

const csv3File = '{{ settings.MEDIA_URL }}{{ job }}/Table3.csv';
const csv3FileInput = csv3File.toString();
const table3Root = document.querySelector("#csv3Root");
const table3Csv = new TableCsv(table3Root);


Papa.parse(csv3File, {
  delimiter: ",",
  download: true,
  skipEmptyLines: true,
  complete: (results) => {
    table3Csv.update(results.data.slice(1), results.data[0]);
  }
});

const csv4File = '{{ settings.MEDIA_URL }}{{ job }}/Table4.csv';
const csv4FileInput = csv4File.toString();
const table4Root = document.querySelector("#csv4Root");
const table4Csv = new TableCsv(table4Root);


Papa.parse(csv4File, {
  delimiter: ",",
  download: true,
  skipEmptyLines: true,
  complete: (results) => {
    table4Csv.update(results.data.slice(1), results.data[0]);
  }
});

const csv5File = '{{ settings.MEDIA_URL }}{{ job }}/Table5.csv';
const csv5FileInput = csv5File.toString();
const table5Root = document.querySelector("#csv5Root");
const table5Csv = new TableCsv(table5Root);


Papa.parse(csv5File, {
  delimiter: ",",
  download: true,
  skipEmptyLines: true,
  complete: (results) => {
    table5Csv.update(results.data.slice(1), results.data[0]);
  }
});

const csv6File = '{{ settings.STATIC_URL }}data/datasource.csv';
const csv6FileInput = csv6File.toString();
const table6Root = document.querySelector("#csv6Root");
const table6Csv = new TableCsv(table6Root);


Papa.parse(csv6File, {
  delimiter: ",",
  download: true,
  skipEmptyLines: true,
  complete: (results) => {
    table6Csv.update(results.data.slice(1), results.data[0]);
  }
});

var source = new ol.source.Vector({
  url: 'bound.geojson',
  format: new ol.format.GeoJSON(),
});

var vectorLayer = new ol.layer.Vector({
  source: source,
});

var center = [{{ stats.centx }}, {{ stats.centy }}]
var view = new ol.View({
  center: ol.proj.fromLonLat(center),
  zoom: 5,
});

var map = new ol.Map({
  layers: [
    new ol.layer.Tile({
      source: new ol.source.OSM({
		url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',
		attributions: ['&copy; <a href="https://www.esri.com/en-us/home">Basemap by Esri</a>']
		}),
    }),
    vectorLayer,
  ],
  target: 'map',
  view: view,
});
var layerExtent = source.getExtent();
var extent = ol.proj.fromLonLat(layerExtent);
view.fit(extent);

searchResultSource.on('addfeature', function() {
  map.getView().fit(extent);
});