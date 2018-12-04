/*var search_query={
  "date_frm": "2018-11-28 03:10:00",
  "date_to": "2018-12-01 15:24:12",
  "cust_id": "0"
}*/
//serverip="192.168.56.101"
search_query={}
const paginationApp = new Vue({
    el: '#pagination-app',
    data: {
        posts: [],
        baseUrl: 'http://'+serverip+':5000/assignment/search',
        page: 1,
        perPage: assperpage,
        pages: [],
    },
    methods: {
        getPosts () {
            //axios.get(this.baseUrl)
            axios({
                    method: 'post',
                    url: this.baseUrl,
                    data: search_query,
                    config: { headers: {'Content-Type': 'application/json' }}
            })
            .then(response => {
                this.posts = response.data.resp;
                console.log(this.posts)
            })
            .catch(response => {
                console.log(response);
            });
            /*
            
             var http = new XMLHttpRequest(); //$.post("http://"+serverip+":5000/assignment",assignmentdict)
                    var url = "http://"+serverip+":5000/assignment/search";
                    var params = JSON.stringify(search_query);
                    http.open("POST", url, true);

                    //Send the proper header information along with the request
                    http.setRequestHeader("Content-type", "application/json");
                    http.onreadystatechange = function() {//Call a function when the state changes.
                        if(http.readyState == 4 && http.status == 200) {

                            this.posts=JSON.parse(http.responseText).resp;
                            console.log(this.posts)
                        }
                    }

            http.send(params);
            */
        },
        setPages () {
            let numberOfPages = Math.ceil(this.posts.length / this.perPage);
            for (let index = 1; index <= numberOfPages; index++) {
                this.pages.push(index);
            }
        },
        paginate (posts) {
            let page = this.page;
            let perPage = this.perPage;
            let from = (page * perPage) - perPage;
            let to = (page * perPage);
            return  posts.slice(from, to);
        },
    },
    computed: {
        displayedPosts () {
            return this.paginate(this.posts);
        }
    },
    watch: {
        posts () {
            this.setPages();
        }
    },
    created () {
        this.getPosts();
    }
});