import strutils, sequtils

const
  a = 1664525'u32
  c = 1013904223'u32

const seed = 0x13371337'u32

const encryptedFlag = @[
  40'u8, 248'u8, 62'u8, 230'u8, 62'u8, 47'u8, 67'u8, 12'u8,
  185'u8, 150'u8, 209'u8, 92'u8, 214'u8, 191'u8, 54'u8, 216'u8,
  32'u8, 121'u8, 14'u8, 142'u8, 82'u8, 33'u8, 178'u8, 80'u8,
  227'u8, 152'u8, 181'u8, 201'u8, 184'u8, 160'u8, 136'u8, 48'u8,
  217'u8, 10'u8
]

proc keystream(seed: uint32, length: int): seq[uint8] =
  var s = seed
  result = newSeq[uint8](length)
  for i in 0 ..< length:
    s = (a * s + c)
    result[i] = uint8(s shr 16)

proc xorEncrypt(input: string, seed: uint32): seq[uint8] =
  let stream = keystream(seed, input.len)
  result = newSeq[uint8](input.len)
  for i in 0 ..< input.len:
    result[i] = uint8(input[i].ord) xor stream[i]

proc main() =
  echo "Enter the flag:"
  let userFlag = readLine(stdin).strip()
  let encryptedInput = xorEncrypt(userFlag, seed)

  if encryptedInput == encryptedFlag:
    echo "Correct!"
  else:
    echo "Incorrect."

main()

