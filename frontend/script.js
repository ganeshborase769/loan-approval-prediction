const API="http://127.0.0.1:8000", $=x=>document.getElementById(x); let token=localStorage.getItem("loan_token");
const show=x=>$(x).classList.remove("hidden"), hide=x=>$(x).classList.add("hidden"), hd=()=>({"Content-Type":"application/json","Authorization":"Bearer "+token});
async function req(p,o={}){let r=await fetch(API+p,o),d={};try{d=await r.json()}catch{}if(!r.ok)throw Error(d.detail||"Request failed");return d}
$("rt").onclick=()=>{show("rf");hide("lf")};$("lt").onclick=()=>{show("lf");hide("rf")};
$("lf").onsubmit=async e=>{e.preventDefault();try{let d=await req("/auth/login",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({email:$("le").value,password:$("lp").value})});token=d.token;localStorage.setItem("loan_token",token);open(d.user)}catch(x){$("msg").textContent=x.message}};
$("rf").onsubmit=async e=>{e.preventDefault();try{let d=await req("/auth/register",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({name:$("rn").value,email:$("re").value,password:$("rp").value})});token=d.token;localStorage.setItem("loan_token",token);open(d.user)}catch(x){$("msg").textContent=x.message}};
function open(u){hide("auth");show("dash");show("logout");$("navUser").textContent=u.name;$("welcome").textContent=u.name.split(" ")[0];load()}
$("logout").onclick=()=>{localStorage.removeItem("loan_token");location.reload()};
$("form").id!=="lf" && 0;
$("form").onsubmit=async e=>{if(e.target.id!=="form")return;e.preventDefault();show("result");let p={Gender:$("Gender").value,Married:$("Married").value,Dependents:$("Dependents").value,Education:$("Education").value,Self_Employed:$("Self_Employed").value,ApplicantIncome:+$("ApplicantIncome").value,CoapplicantIncome:+$("CoapplicantIncome").value,LoanAmount:+$("LoanAmount").value,Loan_Amount_Term:+$("Loan_Amount_Term").value,Credit_History:+$("Credit_History").value,Property_Area:$("Property_Area").value};try{let d=await req("/predict",{method:"POST",headers:hd(),body:JSON.stringify(p)}),ok=d.prediction==="Approved";$("result").className="result "+(ok?"approved":"rejected");$("result").innerHTML=(ok?"✅":"❌")+" Loan "+d.prediction+"<br><small>Confidence: "+d.probability+"%</small>";load()}catch(x){$("result").className="result rejected";$("result").textContent=x.message}};
async function load(){try{let[s,h]=await Promise.all([req("/stats",{headers:hd()}),req("/predictions",{headers:hd()})]);$("total").textContent=s.total;$("approved").textContent=s.approved;$("rejected").textContent=s.rejected;$("rate").textContent=s.approval_rate+"%";$("history").innerHTML=h.map(x=>`<tr><td>${x.created_at}</td><td>${x.applicant_income}</td><td>${x.loan_amount}</td><td>${x.credit_history?"Good":"Poor"}</td><td>${x.property_area}</td><td>${x.prediction}</td><td>${x.probability}%</td></tr>`).join("")||"<tr><td colspan=7>No predictions yet.</td></tr>"}catch{}}
(async()=>{if(token)try{open(await req("/auth/me",{headers:hd()}))}catch{localStorage.removeItem("loan_token")}})();

async function loadAnalytics(){
 try{
  const a=await req("/analytics");
  $("bestModel").textContent="Best model: "+a.best_model;
  $("dsRows").textContent=a.dataset.rows;
  $("dsApproved").textContent=a.dataset.approved;
  $("dsRejected").textContent=a.dataset.rejected;
  $("modelMetrics").innerHTML=a.metrics.map(m=>`<tr><td>${m.model}</td><td>${m.accuracy}%</td><td>${m.precision}%</td><td>${m.recall}%</td><td>${m.f1}%</td></tr>`).join("");
  const cm=a.confusion_matrices[a.best_model]||[[0,0],[0,0]];
  $("confusion").innerHTML=`<div class="head">Actual / Predicted</div><div class="head">Predicted 0</div><div class="head">Predicted 1</div><div class="head">Actual 0</div><div>${cm[0][0]}</div><div>${cm[0][1]}</div><div class="head">Actual 1</div><div>${cm[1][0]}</div><div>${cm[1][1]}</div>`;
 }catch(e){}
}
const oldOpen=open;
open=function(u){oldOpen(u);loadAnalytics()};
