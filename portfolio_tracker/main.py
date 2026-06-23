from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
import models, schemas, database

app = FastAPI(title="Skill & Project Tracker")

models.Base.metadata.create_all(bind=database.engine)

app.mount("/static", StaticFiles(directory="templates"), name="static")

@app.get("/")
def read_root():
    return FileResponse("templates/index.html")

@app.post("/skills/", response_model=schemas.Skill)
def create_skill(skill: schemas.SkillCreate, db: Session = Depends(database.get_db)):
    db_skill = db.query(models.Skill).filter(models.Skill.name == skill.name).first()
    if db_skill:
        raise HTTPException(status_code=400, detail="Skill already registered")
    new_skill = models.Skill(name=skill.name, level=skill.level)
    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)
    return new_skill

@app.get("/skills/", response_model=List[schemas.Skill])
def read_skills(db: Session = Depends(database.get_db)):
    return db.query(models.Skill).all()

@app.post("/projects/", response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(database.get_db)):
    db_skill = db.query(models.Skill).filter(models.Skill.id == project.skill_id).first()
    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill ID not found")
    
    new_project = models.Project(
        title=project.title, 
        description=project.description, 
        skill_id=project.skill_id
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project
@app.delete("/skills/{skill_id}")
def delete_skill(skill_id: int, db: Session = Depends(database.get_db)):
    db_skill = db.query(models.Skill).filter(models.Skill.id == skill_id).first()
    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    db.delete(db_skill)
    db.commit()
    return {"detail": f"Skill {skill_id} successfully deleted"}