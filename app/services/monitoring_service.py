from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from uuid import UUID
from typing import Dict, Any, Tuple, List
from sqlalchemy import select, func, Column, cast, Float

from app.db.models import Debt


async def get_user_summary(db: AsyncSession, user_id: UUID) -> Dict[str, Dict[str, Any]]:
	stmt = (
		select(
			Debt.currency,
			Debt.debt_type,
			cast(func.sum(Debt.amount), Float).label('total')
		)
		.where(Debt.owner_id == user_id)
		.group_by(Debt.currency, Debt.debt_type)
	)
	result = await db.execute(stmt)
	rows: List[Tuple[str, str, float]] = result.all() #type: ignore
	
	summary: Dict[str, Dict[str, Any]] = {}
	

	for currency, debt_type, total in rows:
		if currency not in summary:
			summary[currency] = {"total_owed_to": 0.0, "total_owed_by": 0.0, "net_balance": 0.0}
		key = None
		t = (debt_type or "").lower()
		if t in ("owed_to", "to", "lend", "lent", "credit"):
			key = "total_owed_to"
		elif t in ("owed_by", "by", "borrow", "borrowed", "debit"):
			key = "total_owed_by"
		else:

			key = "total_owed_by"

		summary[currency][key] = float(total)

	# Compute balances
	for currency, data in summary.items():
		data["net_balance"] = data.get("total_owed_to", 0.0) - data.get("total_owed_by", 0.0)

	return summary
