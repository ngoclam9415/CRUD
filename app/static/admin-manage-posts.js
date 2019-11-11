HOST_URL = "http://localhost:8080/blog-posts/"

function generateTableHead(table) {
    let thead = table.createTHead();
    let row = thead.insertRow();
    data = ['#', 'Title', 'Slug', 'URL', 'Modification']
    for (let key of data) {
        let th = document.createElement("th");
        let text = document.createTextNode(key);
        th.appendChild(text);
        row.appendChild(th);
    }
}
function generateTable(table, data) {
    let row = table.insertRow();
    let keys = ['id', 'title', 'slug', 'url', 'modification']
    for (let i = 0; i < keys.length; i++) {
        key = keys[i];
        let cell = row.insertCell();

        let text = document.createTextNode(data[key]);

        if (key == 'url') {
            text = document.createTextNode(HOST_URL + data['slug']);
        }

        if (key == 'modification') {
            button = document.createElement("button");
            button.className = 'mb-2 btn btn-sm btn-primary mr-1'
            button.innerHTML = 'Edit'
            button.id = "button-edit-post-" + data['id']

            button.addEventListener('click', (event) => {
                document.location.href = Flask.url_for('frontend.edit_post', { post_slug: event.target.parentNode.parentNode.getElementsByTagName('td')[2].innerHTML });
                // console.log(event.target.parentNode.parentNode.getElementsByTagName('td')[0].innerHTML)

            }, false);

            button.type = 'button'

            cell.appendChild(button);

            text = document.createElement("button");
            text.className = 'mb-2 btn btn-sm btn-danger mr-1'
            text.type = 'button'

            text.innerHTML = 'Delete'
        }



        cell.appendChild(text);
    }
}




// let POST_API = 'https://original-glider-246113.appspot.com/posts'
let POST_API = 'http://localhost:8080/posts'
fetch(POST_API).then(response => {
    return response.json();
}).then(data => {
    console.log("Day la flow 2", data.data);
    // let posts = data.data;

    $('#pagination-demo').twbsPagination({
        totalPages: data.total_pages,
        visiblePages: 3,
        onPageClick: function (event, page) {
            postsCurrentPage = POST_API + "?page=" + page
            getresult(postsCurrentPage);
        }
    });



}).catch(function (e) {
    console.log("Booo", e);
});


var getresult = (url) => {
    $.ajax({
        url: url,
        type: "GET",
        data: { rowcount: $("#rowcount").val(), "pagination_setting": $("#pagination-setting").val() },
        // beforeSend: function () { $("#overlay").show(); },
        success: function (data) {
            let posts = data.data;
            $("#table-posts tbody").remove();
            $("#table-posts thead").remove();

            for (let pi = 0; pi < posts.length; pi++) {
                const post = posts[pi];

                delete post.status;
                delete post.thumbnail;
                delete post.content;
                delete post.created_at;

                let table = document.querySelector("table");
                generateTable(table, post);

            }
            let table = document.querySelector("table");
            generateTableHead(table);
        },
    });
}

