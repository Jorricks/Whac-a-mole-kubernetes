

function createMole(width){
    const fullWidth = 383;
    const fullHeight = 700;
    const sizeScale = width / fullWidth;

    let $allMoles = $('.all-moles');

    let $resizedMole = $('<div>')
        .addClass('resized-mole')
        .appendTo($allMoles);

    let $aMoleContainer = $('<div>')
        .addClass('a-mole-container')
        // .attr('-webkit-transform', 'scale(' + sizeScale + ')')
        // .attr('-moz-transform', 'scale(' + sizeScale + ')')
        // .attr('-ms-transform', 'scale(' + sizeScale + ')')
        .attr('transform', 'scale(' + sizeScale + ')')
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

    $('<div>')
        .addClass('text')
        .text('IDENTIFIER')
        .appendTo($aMoleContainer);
}