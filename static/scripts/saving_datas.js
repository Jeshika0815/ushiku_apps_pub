// saving_data.js
// 株式会社シラヤマ　牛久工場DX化プロジェクト
// 作成；齊藤巧海-東京情報デザイン専門職大学
// 牛久工場業務管理システム(Ushiku4-1)
// Ver1
// 一部フォーム入力のローカル保存を行う

/*
function getdate_ymd(){
    const nd = new Date()
}
*/
// 全体の作業伝票(CSV出力)
document.addEventListener('DOMContentLoaded', () => {
    let sd = localStorage.getItem('start_date');
    let ed = localStorage.getItem('end_date');
    if(sd) document.getElementById('id_start_date').value = sd;
    if(ed) document.getElementById('id_end_date').value = ed;

    //フォーム送信時に保存をかける
    const form = document.querySelector('form');
    if(form){
        form.addEventListener('submit', function(){
            let start = document.getElementById('id_start_date').value;
            let end = document.getElementById('id_end_date').value;
            localStorage.setItem('start_date',start);
            localStorage.setItem('end_date', end);
        });
    }
});
