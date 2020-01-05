let addComment = function(form_url, comment_text, article_id, commentsListSelector, newCommentInputSelector) {

    let submitData = {text: comment_text, article_id: article_id};

    // Submit the form
    $.ajax({
      data: submitData,
      url: form_url ,
      method: "POST",
      success: function (data) {
          // Append results to div so that jQuery can find results (because results element cannot be top-level)
          let articleCommentsHTML = $('<div></div>').append(data).find(commentsListSelector).html();
          refreshCommentsList(articleCommentsHTML, commentsListSelector, newCommentInputSelector);
      }
    });
};

let refreshCommentsList = function(articleCommentsHTML, commentsListSelector, newCommentInputSelector) {
    let $articleComments = $(commentsListSelector);
    $articleComments.empty();
    $articleComments.html(articleCommentsHTML);
    $(newCommentInputSelector).val('');
};