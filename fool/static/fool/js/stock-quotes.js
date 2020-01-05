$(document).ready(function() {
    $('.shuffle-stock-quotes').click( function() {
        shuffleStockQuoteRows();
    });
});

let shuffleStockQuoteRows = function() {
    let $stockQuoteRows = $('.stock-quote-row');
    let $shuffledStockQuoteRows = shuffle($stockQuoteRows);

    $('.related-stock-quotes-rows').html('');

    $shuffledStockQuoteRows.each(function() {
        $('.related-stock-quotes-rows').append(this);
    })
};

/*
Shuffle:
This function sorts an array in a random order. The method used is as follows:
1) Walk through the array items backwards using a counter
2) Choose a random item in the array
3) Swap the randomly chosen item with the item at the counter index
4) Stop when there are no more items to walk
*/
function shuffle(array) {
    let counter = array.length, temp, index;

    while (counter > 0) {
        // Pick a random index
        index = Math.floor(Math.random() * counter);

        // Decrement counter
        counter--;

        // Swap the randomly chosen element with the item at the counter index
        temp = array[counter];
        array[counter] = array[index];
        array[index] = temp;
    }

    return array;
}