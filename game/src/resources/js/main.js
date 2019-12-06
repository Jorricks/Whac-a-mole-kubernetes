
function createSetup(moles){
    for (let mole in moles){
        mole = parseInt(mole);
        createMole(moles[mole]);
        if (mole % 7 < 4){
            if (mole < moles.length - 1){
                createGap();
            }
        } else {
            createGap();
        }
    }
}

function updateSpecificMole(moleName, alive){
    let $mole = $('#'+moleName);
    console.log($mole);
    $mole.removeClass('ready-mole');
    $mole.removeClass('unready-mole');
    if (alive === "ready"){
        $mole.addClass('ready-mole')
    } else if (alive === "unready"){
        $mole.addClass('unready-mole');
    }
}

function createMole(moleName){
    let $allMoles = $('.all-moles');

    let $resizedMole = $('<div>')
        .attr('id', moleName)
        .addClass('resized-mole')
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

function createGap(){
    let $allMoles = $('.all-moles');
    $('<div>')
        .addClass('no-mole')
        .appendTo($allMoles);
}
