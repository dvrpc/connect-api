from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from data_structures import schemas, database, crud
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/get_user_studies/", response_model=schemas.UserStudies)
def user_studies(
        username: str = None,  # Optional parameter
        schema: str = Query(
            None, description="The schema to use (lts or sidewalk)"),
        db: Session = Depends(database.get_db_for_schema)):

    if username is None:
        db_studies = crud.get_all_projects(db)
    else:
        db_studies = crud.get_projects_by_user(
            db, username)

    if db_studies is None or len(db_studies) == 0:
        return JSONResponse(
            content={"studies": ["No studies have been created yet!"]}
        )
    db_studies_transformed = []
    for item in db_studies:
        study_info = {
            "username": item.username,
            "seg_name": item.seg_name,
            "has_isochrone": item.has_isochrone if item.has_isochrone is not None else False,
            "miles": item.miles if item.miles is not None else 0,
            "total_pop": item.total_pop if item.total_pop is not None else 0,
            "disabled": item.disabled if item.disabled is not None else 0,
            "ethnic_minority": item.ethnic_minority if item.ethnic_minority is not None else 0,
            "female": item.female if item.female is not None else 0,
            "foreign_born": item.foreign_born if item.foreign_born is not None else 0,
            "lep": item.lep if item.lep is not None else 0,
            "low_income": item.low_income if item.low_income is not None else 0,
            "older_adult": item.older_adult if item.older_adult is not None else 0,
            "racial_minority": item.racial_minority if item.racial_minority is not None else 0,
            "youth": item.youth if item.youth is not None else 0,
            "circuit": item.circuit,
            "total_jobs": item.total_jobs if item.total_jobs is not None else 0,
            "bike_ped_crashes": item.bike_ped_crashes if item.bike_ped_crashes is not None else 0,
            "essential_services": item.essential_services if item.essential_services is not None else 0,
            "rail_stations": item.rail_stations if item.rail_stations is not None else 0,
            "deleted": item.deleted if item.deleted is not None else False,
            "shared": item.shared if item.shared is not None else False,
            "geom": str(item.geom)
        }
        db_studies_transformed.append(study_info)

    return {"studies": db_studies_transformed}
