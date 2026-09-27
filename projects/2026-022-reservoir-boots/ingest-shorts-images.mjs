import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
const P=path.dirname(new URL(import.meta.url).pathname);
const jobs=JSON.parse(fs.readFileSync(path.join(P,'04_composition/shorts-image-jobs.json')));
const manifest=JSON.parse(fs.readFileSync(path.join(P,'04_composition/image-sources.json')));
const comments=[
 '물 위의 빈 장화 두 짝, 왼쪽 작은 파란 패치, 인체·정체 노출 없음. 도입 훅과 일치.',
 '따뜻한 출입문 앞 빈 장화 자리. 장화가 사라진 단계와 일치, 인체·귀신 없음.',
 '다섯 손가락의 젖은 손바닥 흔적. 장화 없음. 발자국과 구별되며 인접 컷과 전개 일치.',
 '수면 위 고무 밑창과 물결이 선명함. 장화 형태 정상, 내부 인체 없음.',
 '번갈아 다가오는 빈 장화 두 짝과 좌대 난간. 근접 위협의 단계 유지.',
 '난간 위 한 짝과 물 위 다른 한 짝. 정체·회색 니트·손·결말을 공개하지 않음.'
];
for(const [i,j]of jobs.entries()){
 const relative='assets/visuals/'+j.id+'.png',dest=path.join(P,'04_composition',relative);
 if(fs.existsSync(dest))throw Error('Refusing to overwrite '+dest);
 fs.copyFileSync(j.source,dest);
 const sha256=createHash('sha256').update(fs.readFileSync(dest)).digest('hex');
 manifest.push({...j,file:dest,sha256,render_approved:true,pass_1:'pass',pass_2:'pass',review_note:comments[i]});
}
fs.writeFileSync(path.join(P,'04_composition/image-sources.json'),JSON.stringify(manifest,null,2)+'\n');
fs.appendFileSync(path.join(P,'05_review/image-review.md'),'\n## 독립 쇼츠 이미지: 두 차례 개별 검수\n\n내장 ImageGen으로 각기 새로 생성. 본편 이미지·영상 프레임·참조 이미지는 사용하지 않았다. 생성 직후 개별 원본 확인, 이후 각 원본을 다시 열어 원고와 인접 컷을 대조했다. 최종 여섯 장 모두 통과.\n\n'+jobs.map((j,i)=>`- ${j.id}: 1차 통과 / 2차 통과 / 승인. ${comments[i]} SHA256은 image-sources.json에 기록. 생성 원본: ${j.source}`).join('\n')+'\n\n교체 기록: 최초 short-new-03 (exec-ba5f7ff0-9f26-4684-8ed4-cba46380a2e6.png)은 사라진 장화가 덱에 나타나 원고와 모순되어 제외했다. 장화를 명시적으로 금지한 신규 프롬프트로 exec-ffc4052c-9c22-4348-ab3b-944689baa1b9.png를 생성하고 두 검수를 반복해 통과했다. 제외본은 컴포지션·Git에 포함하지 않는다.\n');
console.log('Six twice-reviewed independent portrait assets copied.');
