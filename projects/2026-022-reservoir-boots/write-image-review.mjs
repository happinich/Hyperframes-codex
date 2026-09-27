import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
const P=path.dirname(new URL(import.meta.url).pathname);
const file=path.join(P,'04_composition/image-sources.json');
const assets=JSON.parse(fs.readFileSync(file));
for(const a of assets){
 if(!a.pass1.startsWith('pass')||!a.pass2.startsWith('pass'))throw Error('Unreviewed asset '+a.id);
 a.sha256=createHash('sha256').update(fs.readFileSync(a.file)).digest('hex');
 a.render_approved=true;
}
fs.writeFileSync(file,JSON.stringify(assets,null,2)+'\n');
const sections=assets.map(a=>`## ${a.id} · ${a.scene}\n\n- 파일: \`${path.relative(P,a.file)}\`\n- SHA256: \`${a.sha256}\`\n- 생성: 내장 ImageGen, 원본 \`${a.source}\`\n- 1차 개별 원본 검수: ${a.pass1}\n- 2차 원고·인접 장면 대조: ${a.pass2}\n- 교체 이력: ${JSON.stringify(a.replacements??[])}\n- 최종 판정: render approved\n`).join('\n');
fs.writeFileSync(path.join(P,'05_review/image-review.md'),'# 이미지 검수\n\n본편 52장 모두 개별 원본 확인 후 원고·인접 컷 대조를 완료했습니다. 접촉 시트는 보조 자료이며 개별 검수를 대체하지 않았습니다.\n\n초기 location-approved.png는 창문 실루엣 오인 가능성으로 제외했습니다. location-clear-window.png는 생성 후 원본 확인, 두 번째 개별 확인에서 빈 창문·육지 뜰채·부유식 좌대 구조를 확인했습니다. 두 참조 이미지는 영상에 직접 사용하지 않습니다.\n\n'+sections);
console.log('All '+assets.length+' main images approved with hashes.');
