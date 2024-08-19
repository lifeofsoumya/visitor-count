from fastapi import FastAPI, Response
from tinydb import TinyDB, Query
import svgwrite

app = FastAPI()

db = TinyDB('visits.json')

if not db.all():
    db.insert({'count': 0})

@app.post('/api/webhook/{username}')
async def webhook(username: str):
    Visit = Query()
    user_record = db.get(Visit.username == username)
    if user_record is None:
        db.insert({'username': username, 'count': 0})
        return {"message": "Visit count incremented"}
    db.update({'count': db.get(Visit.count.exists())['count'] + 1}, Visit.count.exists())
    return {"message": "Visit count incremented"}

@app.get('/api/get-image/{username}')
async def get_image(username: str):
    Visit = Query()
    user_record = db.get(Visit.username == username)
    if user_record is None:
        db.insert({'username': username, 'count': 0})
        user_record = db.get(Visit.username == username)

    visit_count = user_record['count'] + 1
    db.update({'count': visit_count}, Visit.username == username)

    width, height = 210, 50
    rect_width, rect_height = 210, 50

    dwg = svgwrite.Drawing(size=(f"{width}px", f"{height}px"))
    
    gradient = dwg.defs.add(dwg.linearGradient(id="grad", x1="0%", y1="0%", x2="100%", y2="100%"))
    gradient.add_stop_color(0, '#5f6ad5')
    gradient.add_stop_color(1, '#3c47a7')

    dwg.add(dwg.rect(insert=((width - rect_width) / 2, (height - rect_height) / 2), 
                      size=(f"{rect_width}px", f"{rect_height}px"), 
                      rx="20px", ry="20px", fill="url(#grad)"))

    dwg.add(dwg.text(f"Visits: {visit_count}",
                      insert=(f"{width / 2}px", f"{height / 2 + 12}px"),
                      text_anchor="middle",
                      fill="white",
                      font_size="24px",
                      font_family="Verdana"))

    svg_str = dwg.tostring()

    return Response(content=svg_str, media_type="image/svg+xml")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
