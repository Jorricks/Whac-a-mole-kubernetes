$(document).ready(function () {
    $("body").mousemove(function (e) {
        let width = e.pageX;
        let height = e.pageY;
        // console.log(width, height);
        $('.hover-mouse')
            .css('left', width + 'px')
            .css('top', height + 'px');
    })
});

dictOfHashToIPs = {};
killMethod = 'kill';  // Can be either kill or shutdown

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
    $.getJSON('http://localhost/get_pod')
        .done(function (data) {
            if (data.length !== (Object.keys(dictOfHashToIPs).length)) {
                dictOfHashToIPs = {};
                for (let container_index in data) {
                    console.log(data[container_index]);
                    let container = data[container_index];
                    let name = container['metadata']['name'];
                    let hash = name.slice(name.length - 5, name.length);
                    let ip = container['status']['pod_ip'];

                    dictOfHashToIPs[hash] = ip;
                }
                createSetup();
            }

            dict_of_hash_to_status = {};
            for (let container_index in data) {
                console.log(data[container_index]);
                let container = data[container_index];
                let name = container['metadata']['name'];
                let hash = name.slice(name.length - 5, name.length);
                let phase = container['status']['container_statuses'][0]['ready'];

                dict_of_hash_to_status[hash] = phase;
            }
            updateMoleReadyOrNot(dict_of_hash_to_status);
        });
}

function updateMoleReadyOrNot(dict_of_hash_to_status) {
    for (let mole in dict_of_hash_to_status) {
        console.log(dict_of_hash_to_status[mole]);
        if (dict_of_hash_to_status[mole] == false){
            updateSpecificMole(mole.toString(), "unready");
        } else {
            updateSpecificMole(mole.toString(), "ready");
        }
    }
}

function createSetup() {
    let moles = Object.keys(dictOfHashToIPs);
    console.log(moles);

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
    console.log($mole);
    $mole.removeClass('ready-mole');
    // $mole.removeClass('unready-mole');
    if (alive === "ready") {
        $mole.addClass('ready-mole')
    } else if (alive === "unready") {
        // $mole.addClass('unready-mole');
    }
}

function killMole($resizedMole){
    let hash = $resizedMole.attr('molehash');
    let ip = dictOfHashToIPs[hash];
    console.log(hash, ip);
    let url = '';
    if (killMethod === "kill"){
        url = 'http://localhost/relay?ip=' + ip + '&port=8080&link=kill'
    } else if (killMethod === "shutdown"){
        url = 'http://localhost/relay?ip=' + ip + '&port=8080&link=shutdown'
    } else{
        console.error('killMethod has a weird value: ', killMethod);
        return null;
    }
    console.log(url);
    createTextRequest(url, null);
}

function createMole(moleName) {
    let $allMoles = $('.all-moles');

    let $resizedMole = $('<div>')
        .attr('molehash', moleName)
        .addClass('resized-mole')
        .click(function() {
            killMole($(this));
        })
        .appendTo($allMoles);

    let $aMoleContainer = $('<div>')
        .addClass('a-mole-container')
        // .attr('-webkit-transform', 'scale(' + sizeScale + ')')
        // .attr('-moz-transform', 'scale(' + sizeScale + ')')
        // .attr('-ms-transform', 'scale(' + sizeScale + ')')
        // .attr('transform', 'scale(' + sizeScale + ')')
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
        .text(moleName)
        .appendTo($textContainer);

    $('<div>')
        .addClass('unready-indicator')
        .text('almost ready')
        .appendTo($textContainer);
}

function createGap() {
    let $allMoles = $('.all-moles');
    $('<div>')
        .addClass('no-mole')
        .appendTo($allMoles);
}
