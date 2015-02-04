require([
    "plugins/linear_gauge",
    "plugins/gauge",
    "libs/moment.min",
    'libs/jquery'
], function (LinearGauge, JohnGauge) {

    var updateInterval = 60 * 1000;

    $(function(){
        var $tabs = $('#infotabs'),
        initialized = false;
        $tabs.on('tabscreate', function(){
            console.log('Tabs are created');
            addTab($tabs, NAV.urls.room_info_power, 'Power Sensors')
        });
        $tabs.on('tabsload', function(event, ui){
            if (!initialized && ui.tab.prop('id') === 'powercontribtab') {
                initSuperPower();
                initialized = true;
            }
        });
    });

    function addTab(tabs, url, label) {
        console.log('Adding tab to jquery tabs');
        var tab = $('<li id="powercontribtab"><a href="' + url + '">' + label + '</a></li>'),
        tabContent = $('<div id="tabPowerContrib"></div>');
        tabs.find('.ui-tabs-nav').append(tab);
        tabs.append(tabContent);
        tabs.tabs('refresh');
    }

    function initSuperPower() {
        console.log('Let the magic happen.');

        var sensorsContainer = $('#ups-container');
        initPDUs();
        initGauges(sensorsContainer);
        initIODisplay(sensorsContainer);
    }

    function initPDUs() {
        /* Initialize a LinearGauge for each pdu sensor */

        var pdus = {},
        $container = $('#pdu-container');
        $container.find('.apc-sensor').each(function (index, element) {
            var metric = $(element).attr('data-metric');
            pdus[metric] = new LinearGauge({
                nodeId: element.id,
                precision: 1,
                threshold: 7
            });
        });

        createCollector(pdus, 'update', $container);

        $container.on('custom_update', function () {
            $container.find('.last-updated span').html(moment().format('DD.MM, HH:mm:ss'));

            /* Add the sum of the gauges to the display */
            $('.rack').each(function(index, rack) {
                var $rack = $(rack);

                var upsUpperValue = $rack.find('.upsstrom svg:first').attr('data-currentvalue');
                var byUpperValue = $rack.find('.bystrom svg:first').attr('data-currentvalue');
                var sumUpper = +upsUpperValue + +byUpperValue;

                var upsLowerValue = $rack.find('.upsstrom svg:last').attr('data-currentvalue');
                var byLowerValue = $rack.find('.bystrom svg:last').attr('data-currentvalue');
                var sumLower = +upsLowerValue + +byLowerValue;

                $rack.find('.stromsum_upper .currentvalue').text(sumUpper.toFixed(1));
                $rack.find('.stromsum_lower .currentvalue').text(sumLower.toFixed(1));
            });
        });
    }

    function initGauges(sensorsContainer) {
        /* Initialize a gauge for each .gauge-container */

        var gauges = {};
        sensorsContainer.find('.ups-status .gauge-container').each(function (index, element) {
            var $element = $(element),
            invert = false;

            if ($(element).hasClass('charge')) {
                invert = true;  // Invert the colors on this gauge
            }

            gauges[$element.attr('data-metric')] = new JohnGauge({
                nodeId: element.id,
                radius: 70,
                symbol: '%',
                invertScale: invert
            });
        });

        /* Use the 'refresh' function to update all gauges periodically */
        createCollector(gauges, 'refresh');
    }

    function initIODisplay(sensorsContainer) {
        /* Initialize all self-updating values in the IO-Display */

        sensorsContainer.find('.ups-status .io-display').each(function (index, element) {
            var $figure = $(element),
            $nodes = $figure.find('[data-metric]');

            var sensors = {};
            $nodes.each(function () {
                var $node = $(this);
                sensors[$node.attr('data-metric')] = $node;
            });

            createCollector(sensors, 'html', sensorsContainer);
        });

        sensorsContainer.on('custom_update', function () {
            var $box = sensorsContainer.find('.node.input'),
            problem = false;

            /* Update timestamp */
            sensorsContainer.find('.last-updated span').html(moment().format('DD.MM, HH:mm:ss'));

            /* Highlight when input power is below a threshold */
            $box.find('[data-metric]').each(function (index, element) {
                if (element.innerHTML < 200) {
                    problem = true;
                }
            });

            if (problem) {
                $box.addClass('io-alert');
            } else {
                $box.removeClass('io-alert');
            }

        });

    }

    function createCollector(objects, updateFunc, container) {
        /*
          Sets up datacollection and update for the objects.

          Objects is a 'dictionary' with metric as key and object to update
          as value.

          The response from Graphite contains a list of objects for all metrics,
          where the 'target' indicates which metric the data is for.
        */

        var metrics = createMetricList(objects),
        params = getGraphiteUrlParams(metrics);
        setInterval(function () {
            update(params, objects, updateFunc, container);
        }, updateInterval);
        update(params, objects, updateFunc, container);
    }

    function createMetricList(objects) {
        /* Creates a list of metrics from the objects-'keys' */
        var metrics = [];
        for (var metric in objects) {
            if (objects.hasOwnProperty(metric)) {
                metrics.push(metric);
            }
        }
        return metrics;
    }

    function getGraphiteUrlParams(metrics) {
        /* Creates params to post request */
        return {
            'target': metrics,
            'from': '-5min',
            'until': 'now',
            'format': 'json'
        }
    }

    function update(parameters, objects, func, container) {
        /* Fetches json-data from url. Updates value using 'func' for each object */
        $.post(NAV.graphiteRenderUrl, parameters, function (data) {
            for (var i = 0, l = data.length; i < l; i++) {
                var obj = data[i],
                target = obj.target,  // Metric name
                datapoints = obj.datapoints,
                value = datapoints[datapoints.length - 1][0] ||
                    datapoints[datapoints.length - 2][0];
                objects[target][func](value);
            }
            if (container !== undefined) { container.trigger('custom_update'); }
        }, 'json');
    }


    return initSuperPower;

});

