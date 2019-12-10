$(document).ready(function () {
    $("body").mousemove(function (e) {
        let width = e.pageX;
        let height = e.pageY;
        // console.log(width, height);
        $('.hover-mouse')
            .css('left', width + 'px')
            .css('top', height + 'px');
    });

    $('.settings-icon')
        .on('click', function(){
            $('.settings-screen')
                .addClass('visible');
        });

    updateOurUI();
});

dictOfHashToIPs = {};
killMethod = 'kill';  // Can be either kill or shutdown
updateUI = true;
updateSettingsAtBoot = true;

function changeNOReplicas(noReplicas, onDone) {
    console.log('http://localhost/update_no_replicas?no_replicas=' + noReplicas);
    $.getJSON('http://localhost/update_no_replicas?no_replicas=' + noReplicas)
        .done(function (data) {
            if (onDone !== null){
                onDone(data);
            }
        });
}

function updateOurUI() {
    // do whatever you like here
    if (updateUI) {
        updateMoles();
    }
    setTimeout(updateOurUI, 333);
}

function createTextRequest(url, doneFunction) {
    var request = $.ajax({
        url: url,
        dataType: "text"
    });
    if (doneFunction != null) {
        request.done(doneFunction);
    }
}

function updateMoles() {
    $.getJSON('http://localhost/get_pod_info')
        .done(function (data) {
            if (data.length !== (Object.keys(dictOfHashToIPs).length)) {
                dictOfHashToIPs = {};
                for (let container_index in data) {
                    let container = data[container_index];
                    let name = container['metadata']['name'];
                    let hash = name.slice(name.length - 5, name.length);
                    let ip = container['status']['pod_ip'];

                    dictOfHashToIPs[hash] = ip;
                }
                createSetup();
            }

            dictOfHashToStatus = {};
            for (let container_index in data) {
                let container = data[container_index];
                let name = container['metadata']['name'];
                let hash = name.slice(name.length - 5, name.length);
                let ready = container['status']['container_statuses'][0]['ready'];
                let terminated = container['metadata']['deletion_timestamp'];

                dictOfHashToStatus[hash] = (ready) ? 'ready' : 'unready';
                if (terminated !== null) {
                    console.log('Terminated ', hash);
                    dictOfHashToStatus[hash] = 'terminated';
                }
            }
            updateMoleReadyOrNot(dictOfHashToStatus);

            if (updateSettingsAtBoot){
                createSettingsPanel();
                updateSettingsAtBoot = false;
            }
        });
}

function updateMoleReadyOrNot(dictOfHashToStatus) {
    for (let mole in dictOfHashToStatus) {
        let status = dictOfHashToStatus[mole];
        if (status === 'unready') {
            updateSpecificMole(mole.toString(), "unready");
        } else if (status === 'ready') {
            updateSpecificMole(mole.toString(), "ready");
        } else if (status === 'terminated') {
            updateSpecificMole(mole.toString(), "terminating");
        } else {
            console.log('Unknown status: ', status);
        }
    }
}

function createSetup() {
    let moles = Object.keys(dictOfHashToIPs);

    $('.all-moles').html('');

    for (let mole in moles) {
        mole = parseInt(mole);  // This is the integer index in the key array of dict_of_hash_to_ips.
        createMole(moles[mole], status[mole]);
        if (mole % 7 < 4) {
            if (mole < moles.length - 1) {
                createGap();
            }
        } else {
            createGap();
        }
    }
}

function updateSpecificMole(moleName, alive) {
    let $mole = $("div[molehash='" + moleName + "']");

    if ($mole.hasClass('terminating')) {
        // A terminating mole can never become alive anymore
        return;
    }

    if ($mole.hasClass('dead-mole') && alive === 'ready') {
        // Mole is not ready yet. It still has to be detected that it's dead!
        return;
    }


    $mole.removeClass('ready-mole');
    $mole.removeClass('unready-mole');
    $mole.removeClass('dead-mole');
    $mole.removeClass('terminating-mole');
    if (alive === "ready") {
        $mole.addClass('ready-mole')
    } else if (alive === "unready") {
        $mole.addClass('unready-mole');
    } else if (alive === "dead") {
        $mole.addClass('dead-mole');
    } else if (alive === "terminating") {
        $mole.addClass('terminating-mole');
    } else {
        console.log('Unknown argument!: ', alive);
    }
}

function killMole($resizedMole) {
    let hash = $resizedMole.attr('molehash');


    let ip = dictOfHashToIPs[hash];
    let url = '';
    if (killMethod === "kill") {
        url = 'http://localhost/relay?ip=' + ip + '&port=8080&link=kill'
    } else if (killMethod === "shutdown") {
        url = 'http://localhost/relay?ip=' + ip + '&port=8080&link=shutdown'
    } else {
        console.error('killMethod has a weird value: ', killMethod);
        return null;
    }
    createTextRequest(url, function(data){
        console.log(data);
        if(data.includes('Killed') || data.includes('shutdown')){
            updateSpecificMole(hash, 'dead');
        }
    });
}

function createMole(moleName) {
    let $allMoles = $('.all-moles');

    let $resizedMole = $('<div>')
        .attr('molehash', moleName)
        .addClass('resized-mole')
        .click(function () {
            killMole($(this));
        })
        .appendTo($allMoles);

    let $aMoleContainer = $('<div>')
        .addClass('a-mole-container')
        .appendTo($resizedMole);

    let $mole = $('<div>')
        .addClass('mole')
        .appendTo($aMoleContainer);

    $('<img>')
        .attr('src', 'img/mole.png')
        .attr('alt', 'mole')
        .attr('width', 351)
        .attr('height', 463)
        .appendTo($mole);

    let $hole = $('<div>')
        .addClass('hole')
        .appendTo($aMoleContainer);

    $('<img>')
        .attr('src', 'img/molehole.png')
        .attr('alt', 'hole')
        .attr('width', 383)
        .attr('height', 100)
        .appendTo($hole);

    let $belowHole = $('<div>')
        .addClass('below-hole')
        .appendTo($aMoleContainer);

    $('<img>')
        .attr('src', 'img/moleholebelow.png')
        .attr('alt', 'hole')
        .attr('width', 383)
        .attr('height', 471)
        .appendTo($belowHole);

    let $textContainer = $('<div>')
        .addClass('text')
        .appendTo($aMoleContainer);

    $('<div>')
        .addClass('hash-indicator')
        .text(moleName)
        .appendTo($textContainer);

    $('<div>')
        .addClass('unready-indicator')
        .text('restarting')
        .appendTo($textContainer);

    $('<div>')
        .addClass('dead-indicator')
        .text('dead')
        .appendTo($textContainer);

    $('<div>')
        .addClass('terminating-indicator')
        .text('terminating')
        .appendTo($textContainer);
}

function createGap() {
    let $allMoles = $('.all-moles');
    $('<div>')
        .addClass('no-mole')
        .appendTo($allMoles);
}

function updateSettings(){
    $('.settings-screen .card').addClass('loader');

    killMethod = $('.kill-method').val();
    let noReplicas = $('.range-replicas input').val();

    changeNOReplicas(noReplicas, function(data){
        $('.settings-screen .card').removeClass('loader');
    });

    return false;
}

function createSettingsPanel(){
    $('.kill-method').val(killMethod);
    $('.range-replicas input').val(Object.keys(dictOfHashToIPs).length);
    $('.range-replicas .no_replicas').text(Object.keys(dictOfHashToIPs).length);
    return false;
}
