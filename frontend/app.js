async function run() {
  const resp = await fetch('unisport.json')
  const gyms = await resp.json()
  console.log(gyms)
}
run()