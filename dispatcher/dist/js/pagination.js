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
                this.posts = this.posts.sort(function(a,b){
                  // Turn your strings into dates, and then subtract them
                  // to get a value that is either negative, positive, or zero.
                  //console.log(sort_field,sort_order)
                  //console.log(a.assignment[sort_field],b.assignment[sort_field])
                  val= new Date(a.assignment[sort_field].$date) - new Date(b.assignment[sort_field].$date);
                  if (sort_order==="ascending"){
                      return val
                  }
                  if(sort_order==="descending"){
                      return val*-1
                  }
                });
                
            })
            .catch(response => {
                console.log(response);
            });
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