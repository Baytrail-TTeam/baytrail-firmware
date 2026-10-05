#!/usr/bin/env python3
"""Read-only structural Option ROM / VBT validator. Does not execute ROM code."""
import sys,struct,json,hashlib,pathlib

def parse_vbt(b,o):
 def u16(p):return struct.unpack_from('<H',b,p)[0]
 def u32(p):return struct.unpack_from('<I',b,p)[0]
 assert o>=0 and o+48<=len(b),'VBT header out of bounds'
 ver,hs,size=u16(o+20),u16(o+22),u16(o+24)
 assert hs>=48 and hs<=size and o+size<=len(b),'VBT size/header bounds'
 bo=u32(o+28);s=o+bo
 assert bo>=hs and s+22<=o+size,'BDB header bounds'
 assert b[s:s+16]==b'BIOS_DATA_BLOCK ','BDB signature'
 bv,bh,bs=u16(s+16),u16(s+18),u16(s+20)
 assert bh>=22 and bh<=bs and s+bs<=o+size,'BDB bounds'
 blocks=[];p=s+bh
 while p<s+bs:
  assert p+3<=s+bs,'Block header bounds'
  ident=b[p];n=u16(p+1);hdr=3
  if ident==53 and p+4<=s+bs and b[p+3]>=3:
   assert p+8<=s+bs,'MIPI v3 header bounds'
   n=u32(p+4)+5
  assert p+hdr+n<=s+bs,f'Block {ident} payload bounds'
  blocks.append({'id':ident,'offset':p-o,'size':n})
  p+=hdr+n
 return {'signature':b[o:o+20].decode('ascii',errors='replace'),'offset':o,'version':ver,'header_size':hs,'size':size,'checksum_mod256':sum(b[o:o+size])%256,'bdb_offset':bo,'bdb_version':bv,'bdb_header_size':bh,'bdb_size':bs,'blocks':blocks}

def inspect(path):
 b=pathlib.Path(path).read_bytes();r={'file':str(path),'size':len(b),'sha256':hashlib.sha256(b).hexdigest(),'errors':[]}
 if b[:2]==b'\x55\xaa':
  try:
   assert len(b)>=26,'ROM header bounds'
   size=b[2]*512;pc=struct.unpack_from('<H',b,24)[0]
   assert 0<size<=len(b),'ROM length bounds'
   assert pc+24<=size and b[pc:pc+4]==b'PCIR','PCIR bounds/signature'
   vendor,device=struct.unpack_from('<HH',b,pc+4)
   image=struct.unpack_from('<H',b,pc+16)[0]*512
   assert 0<image<=len(b),'PCIR image bounds'
   r['rom']={'header_size':size,'pcir_offset':pc,'vendor':f'{vendor:04x}','device':f'{device:04x}','pcir_image_size':image,'code_type':b[pc+20],'indicator':b[pc+21],'checksum_mod256':sum(b[:size])%256}
   assert sum(b[:size])%256==0,'ROM checksum'
  except (AssertionError,struct.error) as e:r['errors'].append(str(e))
 elif not b.startswith(b'$VBT'):r['errors'].append('Missing 55 AA or raw VBT signature')
 r['vbts']=[];o=0
 while True:
  o=b.find(b'$VBT',o)
  if o<0:break
  try:r['vbts'].append(parse_vbt(b,o))
  except (AssertionError,struct.error) as e:r['errors'].append(f'VBT at {o}: {e}')
  o+=4
 if not r['vbts']:r['errors'].append('No valid VBT')
 return r
if __name__=='__main__':
 r=inspect(sys.argv[1]);print(json.dumps(r,indent=2));sys.exit(bool(r['errors']))
