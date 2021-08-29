
var xmap;

function createTable(N_ROWS)
{
    my_table = $('#data-table').DataTable({
        'pageLength': N_ROWS,
        'select': "api",
        'dom': "Bfrtip",
        fixedHeader: {
            'header': false,
            'footer': false
        },
        'buttons': [
            {   'extend': "excelHtml5",
                'title': "{{ filename }}",
                'text': "Выгрузить в Excel (.xlsx)"  },
            {   'extend': "print",
                'title': "Распечатать",
                'text': "Распечатать"  }
        ],
        'columnDefs': [
            { 'targets': "no-sort", orderable: false }
        ],
        // 'order': [[ 1, "asc" ]],
        'language': {
            'url': "https://cdn.datatables.net/plug-ins/1.10.13/i18n/Russian.json",
        }
    });
}

function cancelTask(task_id)
{
    $('#cancel-task-id').val(task_id);
    $('#cancel-label').text("Задание № " + task_id);
    $('#cancelTaskModal').modal('show');
}

function viewTask(task_id, task_lon, task_lat, task_descr, task_datetime_planned, task_mission_descr, task_place_descr)
{
    $('#view-task-id').text(task_id);
    $('#view-task-lon').text(task_lon);
    $('#view-task-lat').text(task_lat);
    $('#view-task-descr').text(task_descr);
    $('#view-task-datetime-planned').text(task_datetime_planned);
    $('#view-task-mission-descr').text(task_mission_descr);
    $('#view-task-place-descr').text(task_place_descr);

    task_lon = task_lon.toString().replace(/,/, '.');
    task_lat = task_lat.toString().replace(/,/, '.');

    const features = [];
    features.push(new ol.Feature({
        geometry: new ol.geom.Point(ol.proj.fromLonLat([
            task_lon, task_lat
        ]))
    }));

    const vectorSource = new ol.source.Vector({
        features
    });

    const vectorLayer = new ol.layer.Vector({
        source: vectorSource,
        style: new ol.style.Style({
          image: new ol.style.Circle({
            radius: 8,
            fill: new ol.style.Fill({color: 'red'})
          })
        })
    });

    setTimeout(() => {
        xmap = new ol.Map({
        layers: [
            new ol.layer.Tile({
                source: new ol.source.OSM()
            }),
            vectorLayer
        ],
        target: 'xmap',
        view: new ol.View({
            center: ol.proj.transform([task_lon, task_lat], 'EPSG:4326', 'EPSG:3857'),
            zoom: 8
        })
    });
    }, 1000);

    $('#viewTaskModal').modal('show');
}


$(document).ready(function() {
    createTable(10);
    $("#loader").removeClass("block").addClass("nonblock");
    $('#viewTaskModal').on('hidden.bs.modal', function () {
        xmap.setTarget(null);
        xmap = null;
    });
});
